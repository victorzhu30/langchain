# 前面课程中我们用agent架构完成了一个增强版的问答模型，但是遗留了一个问题，就是他没有记忆。这节课，我们就来给他加上memory功能。

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="moonshot-v1-8k", 
                openai_api_base="https://api-sg.moonshot.ai/v1/", 
                temperature=0)

from langchain.chains import LLMMathChain
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
import os

search = GoogleSearchAPIWrapper()

def proxied_google_search(query: str) -> str:
    """
    一个包装函数，在调用 Google 搜索前后临时设置和取消代理。
    """
    proxy_url = "http://127.0.0.1:10808"

    original_http_proxy = os.environ.get("HTTP_PROXY")
    original_https_proxy = os.environ.get("HTTPS_PROXY")
    
    print(f"临时设置代理: {proxy_url}")
    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url
    
    try:
        result = search.run(query)
        return result
    finally:
        print("操作完成，取消临时代理。")
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

tools = [
    Tool(
        name="google_search",
        func=proxied_google_search,
        description="当需要回答有关时事、最新信息或不确定的事实性问题时，应使用此工具进行网络搜索。"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="当你需要进行精确的数学计算或解决数学问题时使用此工具。输入应该是一个完整的数学问题。"
    )
]

# ⭐️ 1. 导入处理记忆的模块
# 这是 LangChain 提供的一个最基础的记忆类型，它会把每一轮的对话（用户输入和 AI 回答）完整地存储下来。
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import MessagesPlaceholder

# ⭐️ 2. 初始化 Memory 对象
# memory_key 必须与 prompt 中的占位符变量名 'chat_history' 完全一致
# return_messages=True 是必须的，因为我们使用的是聊天模型
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# 实例化: 我们告诉 memory 对象，当它向 prompt 提供历史记录时，应该使用 chat_history 这个键。这正好对应了我们 prompt 模板中的 MessagesPlaceholder(variable_name='chat_history')。
# return_messages=True: 因为 ChatPromptTemplate 需要的是一个消息对象列表，而不是一个单一的字符串，所以这个参数必须设置为 True。

from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_openai_tools_agent(llm, tools, prompt)

# ⭐️ 3. 创建 AgentExecutor，并将 memory 对象传递进去
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    memory=memory, # <--- 在这里添加 memory
    verbose=True
)

# --- 5. 连续对话测试 ---

print("--- 对话开始 ---")

# 第一个问题
print("\n[我]: 陈华编程是什么？")
response1 = agent_executor.invoke({"input": "陈华编程是什么？"})
print("\n[AI]:", response1['output'])

print("\n" + "="*50 + "\n")

# 第二个问题，利用了上一轮的记忆
print("\n[我]: 它是由谁开发的？")
response2 = agent_executor.invoke({"input": "它是由谁开发的？"})
print("\n[AI]:", response2['output'])

print("\n" + "="*50 + "\n")

# 我们可以检查一下 memory 中存储的内容
print("--- Memory中的内容 ---")
print(memory.buffer)
