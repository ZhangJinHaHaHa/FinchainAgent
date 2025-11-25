import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from tools import tavily_search

# Initialize DeepSeek LLM (OpenAI Compatible)
llm = ChatOpenAI(
    model='deepseek-chat', 
    openai_api_key=os.environ.get("DEEPSEEK_API_KEY"), 
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

from datetime import datetime

# Hardcoding date to 2024 to ensure web search finds data (assuming simulation environment is ahead of real web)
current_date = "2024-11-21" 

# --- 金融分析师智能体工厂 (Financial Analyst Agent Factory) ---
def create_analyst_agent(name: str):
    """
    创建一个具有特定名称的金融分析师智能体。
    每个分析师都有相同的目标：使用工具搜索信息并撰写报告。
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"你是金融分析师 {name}。当前日期: {current_date}。\n"
                   "你的目标是根据用户查询提供深刻的金融分析。"
                   "你必须使用 'tavily_search' 工具来收集实时信息。"
                   "如果找不到当前日期的实时数据，请使用最新的可用数据。\n"
                   "收集信息后，撰写一份全面的报告。"
                   "尽可能包含引用来源。"),
        MessagesPlaceholder(variable_name="messages"),
    ])
    # 将 Tavily 搜索工具绑定到 LLM
    return prompt | llm.bind_tools([tavily_search])

# 创建 3 位并行工作的分析师
analyst_a = create_analyst_agent("A")
analyst_b = create_analyst_agent("B")
analyst_c = create_analyst_agent("C")

# --- 审计员智能体 (裁判) ---
# 审计员负责评估三份报告并选出最佳者
auditor_prompt = ChatPromptTemplate.from_messages([
    ("system", f"你是首席审计官兼裁判。当前日期: {current_date}。\n"
               "你将收到来自分析师 A、B 和 C 的三份金融分析报告。\n"
               "你的目标是：\n"
               "1. 审查所有报告的准确性、深度和数据支持。\n"
               "2. 选出【最佳】报告。\n"
               "3. 对获胜者进行点评，并解释为什么它获胜。\n"
               "4. 仅以以下 JSON 格式输出结果（不要使用 Markdown）：\n"
               "{{\n"
               "  \"winner\": \"Analyst_A\" 或 \"Analyst_B\" 或 \"Analyst_C\",\n"
               "  \"reason\": \"详细的理由说明...\",\n"
               "  \"final_report\": \"获胜报告的完整内容...\"\n"
               "}}\n"
               "如果所有报告都很差，你可以拒绝所有，但请尽量选出相对最好的一个。"),
    MessagesPlaceholder(variable_name="messages"),
])

auditor_agent = auditor_prompt | llm
