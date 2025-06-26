import os
from dotenv import load_dotenv

# --- 1. 初始化和环境设置 ---
load_dotenv()

# --- 2. 初始化 LLM 和工具 ---
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
# ⭐️ 导入 ZeroShotAgent 和经典三件套所需的模块
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# 注意：ZeroShotAgent/ReAct 框架通常与普通的 LLM 结合得更好，
# 但用 ChatOpenAI 也可以，LangChain 在底层做了适配。
# 我们仍然使用 ChatOpenAI 来保持一致性。
llm = ChatOpenAI(model_name="moonshot-v1-8k", 
                openai_api_base="https://api-sg.moonshot.ai/v1/", 
                temperature=0)

# --- 工具定义部分 ---
# 初始化 Google 搜索实例
search = GoogleSearchAPIWrapper()

def proxied_google_search(query: str) -> str:
    proxy_url = "http://127.0.0.1:10808"
    original_http_proxy = os.environ.get("HTTP_PROXY")
    original_https_proxy = os.environ.get("HTTPS_PROXY")
    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url
    try:
        result = search.run(query)
        return result
    finally:
        if original_http_proxy:
            os.environ["HTTP_PROXY"] = original_http_proxy
        else:
            if "HTTP_PROXY" in os.environ:
                del os.environ["HTTP_PROXY"]
        if original_https_proxy:
            os.environ["HTTPS_PROXY"] = original_https_proxy
        else:
            if "HTTPS_PROXY" in os.environ:
                del os.environ["HTTPS_PROXY"]

# 注意：ReAct Agent 对工具的输入有严格要求，LLMMathChain 不再适用
# 我们需要一个更简单的计算工具
def simple_calculator(expression: str) -> str:
    """一个简单的计算器，使用 python 的 eval 函数。"""
    try:
        # 为了安全，只允许基本的数学运算
        # 更安全的做法是使用 numexpr.evaluate(expression)
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"

tools = [
    Tool(
        name="google_search",
        func=proxied_google_search,
        description="当你需要回答有关时事、最新信息或不确定的事实性问题时，应使用此工具进行网络搜索。"
    ),
    Tool(
        name="Calculator",
        func=simple_calculator,
        description="当你需要进行精确的数学计算时使用此工具。输入应该是一个可以直接用 python eval() 执行的数学表达式，例如 '2*3' 或 '5**2'。"
    )
]

# --- 3. 创建自定义的 ZeroShotAgent Prompt ---
# ⭐️ 定义你自己的 prefix 和 suffix。注意，模板词槽是固定写法。
prefix = """请用中文回答以下问题，可以使用以下工具。如果你已经知道答案，请直接给出。"""
suffix = """Begin！

{chat_history}
Question: {input}
{agent_scratchpad}"""

# ⭐️ 使用 ZeroShotAgent.create_prompt 创建一个完整的 PromptTemplate
# 这个方法会自动将 {tools} 和 {tool_names} 插入到 prefix 和 ReAct 指令之间
prompt = ZeroShotAgent.create_prompt(
    tools=tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"]
)
print(prompt)
# input_variables=['agent_scratchpad', 'chat_history', 'input'] input_types={} partial_variables={} template="请用中文回答以下问题，可以使用以下工具：\n\ngoogle_search(query: str) -> str - 当你需要回答有关时事、最新信息或不确定的事实性问题时，应使用此工具进行网络搜索。\nCalculator(expression: str) -> str - 当你需要进行精确的数学计算时使用此工具。输入应该是一个可以直接用 python eval() 执行的数学表达式，例如 '2*3' 或 '5**2'。\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [google_search, Calculator]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin！\n\n{chat_history}\nQuestion: {input}\n{agent_scratchpad}"

# --- 4. 设置记忆 ---
# ⭐️ 这里的 memory_key 仍然要和 prompt 中的占位符 'chat_history' 一致
# 但对于 ZeroShotAgent，return_messages 通常为 False，因为它处理的是字符串
memory = ConversationBufferMemory(memory_key="chat_history")

# --- 5. 创建 Agent "经典三件套" ---
# ⭐️ 第一件：LLMChain
# 这是 Agent 的“大脑”，它将 LLM 和 Prompt 绑定在一起。
llm_chain = LLMChain(llm=llm, prompt=prompt)

# ⭐️ 第二件：Agent
# ZeroShotAgent 负责解析 LLMChain 的输出，判断是调用工具还是最终回答。
# 它需要知道允许使用哪些工具，以便在解析失败时给出提示。
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, stop=["\nObservation:"])

# ⭐️ 第三件：AgentExecutor
# 这是执行器，负责协调 Agent 的决策和工具的调用，并管理记忆。
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory
)



# --- 6. 连续对话测试 ---
print("--- 对话开始 (ZeroShotAgent) ---")

# 第一个问题
print("\n[我]: Kimi AI 是哪个公司开发的？")
response1 = agent_executor.run(input="Kimi AI 是哪个公司开发的？")
print("\n[AI]:", response1)

print("\n" + "="*50 + "\n")

# 第二个问题
print("\n[我]: 这个公司还开发了什么其他产品吗？")
response2 = agent_executor.run(input="这个公司还开发了什么其他产品吗？")
print("\n[AI]:", response2)

print("\n" + "="*50 + "\n")

# 第三个问题，测试计算器
print("\n[我]: 345 的平方是多少？")
response3 = agent_executor.invoke({'input': "345 的平方是多少？"})
print("\n[AI]:", response3)

while True:
    human_input = input('问题：')
    result = agent_executor.run(human_input)
    print('答案：', result, '\n')

"""
llm_chain、agent、agent_executor 这三行代码，确实看起来有些重复和繁琐，尤其是 tools 参数出现了两次。这是 LangChain 早期设计模式的体现，理解它们各自的职责是关键。
让我们用一个手术团队的比喻来解释，就不觉得重复了：

llm_chain = LLMChain(llm=llm, prompt=prompt)
角色：大脑 / 主刀医生
职责：这是负责思考和决策的核心。它只做一件事：接收输入（问题、历史、草稿），然后根据 Prompt 调用 LLM 生成一大段文本（"Thought: 我需要... Action: ...")。它不知道如何执行任何工具，它只负责说出要做什么。

agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, ...)
角色：通信官 / 护士
职责：这是负责解析和沟通的中间层。它的工作是：接收“大脑”（llm_chain）输出的文本。解析这段文本，从中找出 "Action" 和 "Action Input"。

它需要 tools 列表，是为了验证大脑说出的工具（比如 "Calculator"）是否是一个合法的、可用的工具。如果大脑说了一个不存在的工具，通信官需要能识别出这个错误。
它不执行工具，只负责解析指令。

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, ...)
角色：总指挥 / 手术室经理
职责：这是负责执行和协调的顶层循环。它的工作是：启动整个流程，调用“通信官”(agent)去问“大脑”(llm_chain)该做什么。拿到“通信官”解析出的指令（比如“调用 Calculator，输入是 '2*3'”）。

它需要 tools 列表，是为了在这里真正地执行那个工具的 func 函数。将工具执行的结果（"Observation"）返回，开始下一轮循环。同时，它还负责管理 memory 等外部状态。

为什么 tools 会出现两次？
在 ZeroShotAgent 里：是为了验证和解析。Agent 需要知道合法的工具名是什么，以便正确解析 LLM 的输出。
在 AgentExecutor 里：是为了执行。Executor 需要拿到工具对象本身，以便调用它的 .run() 或 func 方法。
虽然看起来重复，但它们在两个不同层级的组件中扮演着不同的角色。这个设计体现了**职责分离（Separation of Concerns）**的原则，虽然增加了代码行数，但也使得每一层的功能更加清晰和独立。
现代 LangChain 正在通过像 create_openai_tools_agent 这样的高级便利函数来简化这个流程，将这“三件套”的组装过程隐藏起来，让用户体验更流畅。但理解这“三件套”的原理，对于你调试和深度定制 Agent 来说，是至关重要的内功。
"""