import os
from dotenv import load_dotenv
# 在导入其他模块之前加载环境变量，确保 API Key 可用
load_dotenv()

import json
from typing import TypedDict, Annotated, List, Union, Dict
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from agents import analyst_a, analyst_b, analyst_c, auditor_agent, llm
from tools import tavily_search, record_on_chain, token_manager
from html_generator import generate_html_report
import operator

# --- 定义图的状态 (State) ---
# AgentState 用于在图中的各个节点之间传递数据
class AgentState(TypedDict):
    # messages: 保存对话历史，使用 operator.add 进行追加更新
    messages: Annotated[List[BaseMessage], operator.add]
    
    # 追踪每位分析师生成的最新报告内容
    report_a: str
    report_b: str
    report_c: str
    
    # 审计员给出的反馈 (用于第二轮优化)
    feedback_a: str
    feedback_b: str
    feedback_c: str
    
    # 当前轮次 (0: 初稿, 1: 终稿)
    round_count: int
    
    # 最终决策结果
    winner: str          # 获胜的分析师 (例如 "Analyst_A")
    audit_reason: str    # 审计员选择该获胜者的详细理由
    final_report: str    # 最终获胜的报告全文
    block_hash: str      # 上链后的区块哈希值

# --- 节点定义 (Nodes) ---

def run_analyst(agent, name, state, report_key, feedback_key):
    """
    运行分析师智能体的辅助函数。
    支持两轮模式：
    - 第一轮：根据用户查询撰写初稿。
    - 第二轮：根据审计员的反馈优化报告。
    """
    user_query = state['messages'][0]
    current_round = state.get('round_count', 0)
    feedback = state.get(feedback_key, "")
    
    print(f"  [分析师 {name}] 正在思考与工作 (第 {current_round + 1} 轮)...")
    
    # 构建输入消息
    messages = [user_query]
    
    # 如果是第二轮，添加反馈信息
    if current_round > 0 and feedback:
        print(f"    [分析师 {name}] 收到反馈: {feedback[:50]}...")
        feedback_msg = HumanMessage(content=f"这是审计员对你上一轮报告的反馈：\n{feedback}\n\n请根据此反馈修改并优化你的报告。")
        messages.append(feedback_msg)
    
    # 简单的 ReAct 循环
    for _ in range(5): 
        response = agent.invoke(messages)
        messages.append(response)
        
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call['name'] == 'tavily_search':
                    print(f"    [分析师 {name}] 正在搜索: {tool_call['args']['query']}")
                    try:
                        res = tavily_search.invoke(tool_call['args']['query'])
                    except Exception as e:
                        res = str(e)
                    
                    messages.append(ToolMessage(
                        tool_call_id=tool_call['id'], 
                        name=tool_call['name'], 
                        content=str(res)
                    ))
        else:
            return {report_key: response.content}
            
    return {report_key: messages[-1].content}

def analyst_a_node(state: AgentState):
    return run_analyst(analyst_a, "A", state, "report_a", "feedback_a")

def analyst_b_node(state: AgentState):
    return run_analyst(analyst_b, "B", state, "report_b", "feedback_b")

def analyst_c_node(state: AgentState):
    return run_analyst(analyst_c, "C", state, "report_c", "feedback_c")

def auditor_node(state: AgentState):
    """
    审计员节点：
    - 第一轮：生成针对每位分析师的改进建议 (Critique)。
    - 第二轮：评选最终获胜者 (Judge)。
    """
    current_round = state.get('round_count', 0)
    
    if current_round == 0:
        print("  [审计员] 正在进行第一轮评审，生成改进建议...")
        input_text = (
            f"用户查询: {state['messages'][0].content}\n\n"
            f"--- 分析师 A 初稿 ---\n{state.get('report_a', '无')}\n\n"
            f"--- 分析师 B 初稿 ---\n{state.get('report_b', '无')}\n\n"
            f"--- 分析师 C 初稿 ---\n{state.get('report_c', '无')}\n\n"
            "请分别为这三份报告提供简短、具体的改进建议（优缺点分析）。\n"
            "请以 JSON 格式输出，键为 'feedback_a', 'feedback_b', 'feedback_c'。"
        )
        
        response = auditor_agent.invoke([HumanMessage(content=input_text)])
        content = response.content
        
        # 解析 JSON
        import json
        try:
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "{" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
            else:
                json_str = content
            data = json.loads(json_str)
        except:
            print("  [审计员] 解析反馈失败，使用通用反馈。")
            data = {
                "feedback_a": "请补充更多数据支持。",
                "feedback_b": "请补充更多数据支持。",
                "feedback_c": "请补充更多数据支持。"
            }
            
        return {
            "feedback_a": data.get("feedback_a", "无反馈"),
            "feedback_b": data.get("feedback_b", "无反馈"),
            "feedback_c": data.get("feedback_c", "无反馈"),
            "round_count": 1 # 进入下一轮
        }
        
    else:
        print("  [审计员] 正在进行最终评审，选出获胜者...")
        input_text = (
            f"用户查询: {state['messages'][0].content}\n\n"
            f"--- 分析师 A 终稿 ---\n{state.get('report_a', '无')}\n\n"
            f"--- 分析师 B 终稿 ---\n{state.get('report_b', '无')}\n\n"
            f"--- 分析师 C 终稿 ---\n{state.get('report_c', '无')}\n\n"
            "请选出最佳报告。\n"
            "输出 JSON: { 'winner': 'Analyst_X', 'reason': '...', 'final_report': '...' }"
        )
        
        response = auditor_agent.invoke([HumanMessage(content=input_text)])
        content = response.content
        
        import json
        try:
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "{" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
            else:
                json_str = content
            data = json.loads(json_str)
        except:
            data = {"winner": "Analyst_A", "reason": "解析失败，默认选择 A", "final_report": state.get("report_a")}
            
        print(f"  [审计员] 最终获胜者: {data.get('winner')}")
        return {
            "winner": data.get("winner"),
            "audit_reason": data.get("reason"),
            "final_report": data.get("final_report"),
            "messages": [response]
        }

def blockchain_node(state: AgentState):
    """
    区块链节点：将获胜结果上链，分发代币奖励，并生成 HTML 研报。
    """
    winner = state['winner']
    report = state['final_report']
    reason = state['audit_reason']
    
    # 准备上链数据
    data_to_record = {
        "winner": winner,
        "report_snippet": report[:100] + "...", # 仅记录摘要以节省空间
        "reason": reason,
        "status": "VERIFIED" # 已验证
    }
    
    print("  [区块链] 正在记录结果...")
    block_res = record_on_chain.invoke(json.dumps(data_to_record))
    
    # 提取区块哈希
    block_hash = "UNKNOWN"
    # tools.py 返回的是中文 "已上链。区块哈希: {hash}"
    if "区块哈希: " in block_res:
        block_hash = block_res.split("区块哈希: ")[1].strip()
    elif "Block Hash: " in block_res: # 保留英文兼容性
        block_hash = block_res.split("Block Hash: ")[1].strip()
    
    # 分发代币奖励
    print("  [代币经济] 正在分发奖励...")
    reward_msg = token_manager.reward_agent(winner, 100, "赢得最佳分析报告")
    print(f"    - {reward_msg}")
    
    # 生成 HTML 研报
    query = state['messages'][0].content
    html_path = generate_html_report(query, winner, report, reason, block_hash, reward_msg)
    print(f"  [系统] HTML 研报已生成: {html_path}")
    
    # 自动打开 HTML 文件 (适用于 macOS)
    os.system(f"open {html_path}")
    
    return {"block_hash": block_hash}

# --- 边逻辑 (Edges) ---

def auditor_router(state: AgentState):
    """
    决定下一步去哪里：
    - 如果 round_count == 1 (刚完成第一轮评审)，回到分析师进行修改。
    - 如果 round_count == 1 且已经修改过（这里逻辑要注意，auditor 更新了 round_count 到 1，
      说明刚给完反馈，所以应该回分析师。
      但是分析师跑完后，round_count 还是 1，再进 auditor，auditor 发现是 1，就做最终评审。
      评审完后，怎么去 blockchain？
      我们需要一个状态来区分 "去修改" 还是 "去上链"。
    
    修正逻辑：
    - 初始 round_count = 0.
    - Analyst 跑完 -> Auditor.
    - Auditor 发现 round_count == 0 -> 生成反馈 -> 设置 round_count = 1 -> 返回 "revise".
    - Analyst 跑完 (此时 round_count=1) -> Auditor.
    - Auditor 发现 round_count == 1 -> 最终评审 -> 返回 "finalize".
    """
    # 这里的 state['round_count'] 是 Auditor 刚刚更新后的值
    # 如果 Auditor 刚把 0 变成了 1，说明需要修改
    # 但是 Analyst 跑完后进 Auditor 时，round_count 是 1，Auditor 不会变它，
    # 此时 Auditor 跑完 judge 逻辑，我们怎么知道是 judge 完了？
    # 我们可以检查 state 中是否有 'winner'。如果有，说明 judge 完了。
    
    if state.get('winner'):
        return "finalize"
    else:
        return "revise"

# --- 图构建 (Graph Construction) ---

workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("analyst_a", analyst_a_node)
workflow.add_node("analyst_b", analyst_b_node)
workflow.add_node("analyst_c", analyst_c_node)
workflow.add_node("auditor", auditor_node)
workflow.add_node("blockchain", blockchain_node)

# 设置分发器节点
def dispatcher(state):
    return {} 

workflow.add_node("dispatcher", dispatcher)
workflow.set_entry_point("dispatcher")

# 分发器 -> 分析师
workflow.add_edge("dispatcher", "analyst_a")
workflow.add_edge("dispatcher", "analyst_b")
workflow.add_edge("dispatcher", "analyst_c")

# 分析师 -> 审计员
workflow.add_edge("analyst_a", "auditor")
workflow.add_edge("analyst_b", "auditor")
workflow.add_edge("analyst_c", "auditor")

# 审计员 -> (修改 或 上链)
workflow.add_conditional_edges(
    "auditor",
    auditor_router,
    {
        "revise": "dispatcher", # 回到分发器，再次触发三个分析师
        "finalize": "blockchain"
    }
)

workflow.add_edge("blockchain", END)

app = workflow.compile()

# --- 执行入口 (Execution) ---

if __name__ == "__main__":
    print("=== FinChain-Agent 演示 (并行竞争模式) ===")
    user_query = input("请输入您的金融查询: ")
    
    initial_state = {"messages": [HumanMessage(content=user_query)]}
    
    print("\n启动并行分析任务...")
    # 增加递归限制以防止复杂任务中断
    for event in app.stream(initial_state, {"recursion_limit": 100}):
        pass # 输出已在节点内部打印
