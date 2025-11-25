import os
from langchain_core.tools import tool
from tavily import TavilyClient
from utils import calculate_hash, get_timestamp

# Initialize Tavily Client
# Note: In a real app, we'd handle missing keys more gracefully
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

@tool
def tavily_search(query: str):
    """
    使用 Tavily API 搜索金融新闻和分析。
    针对金融主题进行了优化。
    """
    try:
        # 增强的搜索参数，用于金融上下文
        response = tavily_client.search(
            query, 
            search_depth="advanced", 
            topic="finance",
            days=7, # 关注最近 7 天的新闻
            include_answer=True,
            max_results=5
        )
        
        # 格式化输出，使其对智能体更友好
        results = []
        if response.get('answer'):
            results.append(f"摘要回答: {response['answer']}")
        
        for res in response.get('results', []):
            results.append(f"标题: {res['title']}\n链接: {res['url']}\n内容: {res['content']}\n---")
            
        return "\n\n".join(results)
    except Exception as e:
        return f"搜索执行错误: {e}"

class TokenManager:
    def __init__(self, ledger_file="token_ledger.json"):
        self.ledger_file = ledger_file
        self.balances = self._load_ledger()

    def _load_ledger(self):
        """加载代币账本"""
        if os.path.exists(self.ledger_file):
            try:
                import json
                with open(self.ledger_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        # 初始分配：系统 DAO 拥有 100万 FCA
        return {"AnalystAgent": 0, "AuditAgent": 0, "SystemDAO": 1000000}

    def _save_ledger(self):
        """保存代币账本"""
        import json
        with open(self.ledger_file, 'w') as f:
            json.dump(self.balances, f, indent=4)

    def reward_agent(self, agent_name: str, amount: int, reason: str):
        """
        奖励智能体 FCA 代币。
        """
        if agent_name not in self.balances:
            self.balances[agent_name] = 0
        
        self.balances[agent_name] += amount
        self.balances["SystemDAO"] -= amount
        self._save_ledger()
        return f"奖励: {amount} FCA 给 {agent_name}，原因: {reason}。新余额: {self.balances[agent_name]} FCA"

    def get_balance(self, agent_name: str):
        return self.balances.get(agent_name, 0)

# 实例化代币管理器
token_manager = TokenManager()

class BlockchainMock:
    def __init__(self, ledger_file="blockchain_ledger.json"):
        self.ledger_file = ledger_file
        self.chain = []
        # 如果存在，加载现有区块链
        if os.path.exists(ledger_file):
            try:
                import json
                with open(ledger_file, 'r') as f:
                    self.chain = json.load(f)
            except:
                self.chain = []

    def add_block(self, data: dict):
        """
        模拟向区块链添加区块。
        """
        timestamp = get_timestamp()
        # 创建区块内容
        block = {
            "index": len(self.chain) + 1,
            "timestamp": timestamp,
            "data": data,
            "previous_hash": self.chain[-1]["hash"] if self.chain else "0",
        }
        # 计算当前区块的哈希
        block["hash"] = calculate_hash(block)
        
        self.chain.append(block)
        self._save_ledger()
        return block

    def _save_ledger(self):
        import json
        with open(self.ledger_file, 'w') as f:
            json.dump(self.chain, f, indent=4)

# 实例化模拟区块链
blockchain = BlockchainMock()

@tool
def record_on_chain(data: str):
    """
    将最终的分析和审计结果记录到模拟区块链上。
    返回包含哈希的区块详情。
    """
    # 我们期望 data 是 JSON 字符串或字典。
    # 为了简单起见，如果不是字典，我们将其视为字符串负载。
    try:
        import json
        parsed_data = json.loads(data)
    except:
        parsed_data = {"content": data}
        
    block = blockchain.add_block(parsed_data)
    return f"已上链。区块哈希: {block['hash']}"
