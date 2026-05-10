Secure your agents at: CodeAstra.dev

## AI Agent Privacy Notice

Astra Sentinel found a possible pattern where sensitive user, customer, or patient data may be passed directly into an AI agent or LLM context.

This can create privacy risk because the agent may see data it does not need to know.

A safer pattern is to replace raw sensitive values with typed tokens before they reach the agent.

Example:

Before: Book appointment for John Smith, DOB 04/12/1988
After: Book appointment for [CVT:NAME:patient_name], DOB [CVT:DOB:patient_dob]

The agent can still perform the workflow, but it never sees the raw sensitive data.

Detected pattern examples:
```json
[
  {
    "pattern": "unprotected_ai_context",
    "evidence": "agent.invoke(messages)"
  }
]
```

This notice was generated from a privacy scan. Please review before merging.

Secure your agents at: CodeAstra.dev

---

# FinChain-Agent: 去中心化可溯源金融分析智能体网络 (Demo)

## 📖 项目简介

**FinChain-Agent** 是一个基于 **LangChain** 和 **LangGraph** 构建的高级多智能体（Multi-Agent）协作系统。该系统模拟了一个去中心化的金融分析市场，引入了**并行竞争机制**和**代币经济模型**。

在这个系统中，三位独立的 AI 金融分析师并行工作，对同一问题进行深度研究。一位首席审计官（Auditor）作为裁判，评选出最佳分析报告。获胜者将获得 **FCA 代币** 奖励，且其报告会被永久记录在模拟区块链上，并生成精美的 HTML 研报。

## ✨ 核心特性

- **🏎️ 并行竞争与迭代优化 (Iterative Competition)**:
  - **第一轮 (Draft)**: 三位分析师并行撰写初稿。
  - **中场点评 (Critique)**: 审计员对三份初稿进行优缺点点评，提出改进建议。
  - **第二轮 (Refinement)**: 分析师根据反馈优化报告。
  - **最终决选 (Final Judge)**: 审计员选出优化后的最佳报告。

- **⚖️ 智能审计与裁判 (AI Judge)**:
  - **首席审计官 (Chief Auditor)**: 既是导师也是裁判，负责提供反馈和最终裁决。

- **💰 代币经济系统 (Token Economy)**:
  - **FCA Token**: 内置原生代币系统。
  - **激励机制**: 只有获胜的分析师会获得 **100 FCA** 奖励，审计员获得 **20 FCA** 基础工资。系统自动维护 `token_ledger.json` 账本。

- **📄 自动化精美研报 (Premium HTML Report)**:
  - 每次分析结束后，自动生成包含区块链哈希、获胜理由和完整分析的 HTML 格式研报，并自动在浏览器中打开。

- **🔗 模拟区块链存证 (Blockchain Mock)**:
  - 获胜报告的哈希值（Hash）会被计算并记录在 `blockchain_ledger.json` 中，确保证据不可篡改。

## 🛠️ 技术栈

- **Python 3.10+**
- **LangChain / LangGraph**: 复杂的并行状态图编排
- **DeepSeek API**: 高性能大语言模型 (OpenAI 兼容)
- **Tavily API**: 深度金融搜索 (Topic: Finance)
- **HTML/CSS**: 自动化报表生成

## 🚀 快速开始

### 1. 环境准备

确保你已安装 Conda，并创建专用环境：

```bash
# 创建并激活环境
conda create -n FinchainAgent python=3.11
conda activate FinchainAgent

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

在项目根目录下创建一个 `.env` 文件：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 3. 运行系统

运行主程序，开启并行分析流程：

```bash
python main.py
```

**示例输入**:
> "分析比特币和以太坊过去一周的市场表现及未来趋势"

系统将自动：
1. 启动 3 位分析师并行搜索与写作（初稿）。
2. 审计员给出改进建议。
3. 分析师根据建议修改（终稿）。
4. 审计员评选最佳方案。
5. 发放代币奖励并生成研报。

### 4. 验证数据

- **查看代币账本**: `token_ledger.json`
- **查看区块链记录**: `blockchain_ledger.json`
- **查看研报**: `financial_report.html`

## 🧩 工作流原理 (Workflow)

```mermaid
graph TD
    User[用户请求] --> Dispatcher{任务分发}
    
    subgraph Round 1 & 2 [并行分析与迭代]
        Dispatcher --> AnalystA[分析师 A]
        Dispatcher --> AnalystB[分析师 B]
        Dispatcher --> AnalystC[分析师 C]
        
        AnalystA <-->|Tavily Search| ToolsA[工具调用]
        AnalystB <-->|Tavily Search| ToolsB[工具调用]
        AnalystC <-->|Tavily Search| ToolsC[工具调用]
        
        AnalystA --> Auditor[首席审计官]
        AnalystB --> Auditor
        AnalystC --> Auditor
        
        Auditor -->|反馈建议 (Round 1)| Dispatcher
    end
    
    Auditor -->|最终评选 (Round 2)| Blockchain[上链存证]
    
    subgraph Post Processing [后处理阶段]
        Blockchain --> Token[代币分发]
        Token --> HTML[生成 HTML 研报]
    end
    
    HTML --> End[结束]
```

## 📂 项目结构

```
FinChain-Agent/
├── agents.py           # 智能体工厂 (创建 A, B, C, Auditor)
├── main.py             # LangGraph 并行工作流编排
├── tools.py            # Tavily搜索, 区块链Mock, 代币管理器
├── html_generator.py   # HTML 研报生成器
├── utils.py            # 哈希计算工具
├── verify_tokens.py    # 代币系统验证脚本
├── requirements.txt    # 依赖列表
├── blockchain_ledger.json # 区块链账本 (自动生成)
├── token_ledger.json      # 代币账本 (自动生成)
└── financial_report.html  # 最新研报 (自动生成)
```

## ⚠️ 注意事项

- **API 消耗**: 由于同时运行 3 个分析师，Token 消耗量是单智能体模式的 3 倍左右，请留意 API 额度。
- **搜索质量**: 系统已配置 Tavily 的 `finance` 主题和 `advanced` 深度，以确保获取高质量金融数据。