# pip install langchain-community tavily-python "langchain[agents]"

import math
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool

# --- 解决方案：使用为现代模型设计的 Agent (The Modern Way) ---

# 1. 初始化 LLM
# 将 temperature 设置为 0，让模型在遵循指令时更稳定，减少创意发挥
llm = ChatOpenAI(model_name="moonshot-v1-8k", temperature=0)

# 2. 定义可用的工具
# TavilySearchResults 是一个强大的工具，它能联网搜索，也能处理数学计算
# 这是比 llm-math 更现代、更可靠的选择。
# 需要设置 TAVILY_API_KEY 环境变量。
# tools = [TavilySearchResults(max_results=1)]

# 2. 创建一个专门的数学工具 ---
# 使用 @tool 装饰器创建一个简单的 Python 函数作为工具
# 函数的文档字符串 (docstring) 会自动成为 Agent 能看到的工具描述，这非常重要！
@tool
def calculator(expression: str) -> str:
    """当需要进行数学计算或回答关于数学的问题时，使用此工具。输入应该是一个有效的数学表达式。"""
    try:
        # 使用 Python 的 eval 函数来计算表达式，前面加上 math 模块使其能处理更复杂的数学运算
        # 注意：在生产环境中使用 eval 需要非常小心，因为它可能执行任意代码。这里为了演示。
        # 更安全的方式是使用 numexpr.evaluate(expression).item()
        return str(eval(expression, {"__builtins__": None}, {"math": math}))
    except Exception as e:
        return f"计算出错: {e}"
tools = [calculator]

# 3. 拉取一个预设的 Agent 提示模板
# "hwchase17/openai-tools-agent" 是专门为支持工具调用的模型设计的。这个模板指导 LLM 如何使用工具
prompt = hub.pull("hwchase17/openai-tools-agent")
# 你可以 print(prompt.messages) 看看它的内容，它会指导LLM如何格式化工具调用

# 4. 创建 Agent
# Agent 的核心是 LLM + Prompt + Tools
# 它将 LLM、工具和提示组合成一个逻辑单元。
agent = create_openai_tools_agent(llm, tools, prompt)

# 5. 创建 Agent 执行器
# 这是真正运行 Agent 的组件，它负责调用 Agent、执行工具、并将结果传回，直到任务完成。
# verbose=True 会打印出 Agent 的完整思考过程，强烈建议开启以用于调试和理解！
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) 

# 6. 执行任务
# 注意：我们用 invoke 并传入一个字典，这是 LCEL 的标准做法。
# 用自然语言提问，而不是直接给一个表达式，这样LLM更容易理解意图
question = "请使用工具来计算 3.14 的 6.5 次方。"
result = agent_executor.invoke({"input": question})

print("\n--- Agent 执行结果 ---")
# result 是一个字典，'output' 键包含最终答案
print(f"Agent 返回的最终答案: {result['output']}")