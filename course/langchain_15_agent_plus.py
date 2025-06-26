# 前面课程中，介绍了自定义Agent，来增强大模型能力的方法。
# 有了Agent机制之后不仅可以增强大模型的能力，而且项目架构也可以进行调整了.
# 我们把大模型也当做一个Agent，然后让Agent自动取判断场景，然后决定调用哪个Agent。
# 可以说有了Agent之后，我们的应用才有点智能体的意思了。

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="moonshot-v1-8k", 
                openai_api_base="https://api-sg.moonshot.ai/v1/", 
                temperature=0)

# 新增导入：用于数学计算的 Chain
from langchain.chains import LLMMathChain

# 新增：初始化数学计算工具
# 这个 Chain 会把自然语言的数学问题（如“345乘以1.23等于多少？”）
# 转换成 Python 代码并执行，以确保结果精确。
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
import os

search = GoogleSearchAPIWrapper()
# proxy_url = "http://127.0.0.1:10808" 
# os.environ["HTTP_PROXY"] = proxy_url
# os.environ["HTTPS_PROXY"] = proxy_url

# ⭐️ 关键部分：为 Google 搜索创建一个带代理的包装函数 ⭐️
def proxied_google_search(query: str) -> str:
    """
    一个包装函数，在调用 Google 搜索前后临时设置和取消代理。
    """
    proxy_url = "http://127.0.0.1:10808"
    
    # 1. 保存当前的代理设置（如果有的话）
    original_http_proxy = os.environ.get("HTTP_PROXY")
    original_https_proxy = os.environ.get("HTTPS_PROXY")
    
    print(f"临时设置代理: {proxy_url}")
    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url
    
    try:
        # 2. 在 try 块中执行需要代理的操作
        result = search.run(query)
        return result
    finally:
        # 3. 在 finally 块中恢复原始的代理设置（这步至关重要！）
        print("操作完成，取消临时代理。")
        if original_http_proxy:
            os.environ["HTTP_PROXY"] = original_http_proxy
        else:
            # 如果原来没有设置，就删除这个环境变量
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
        # ⚠️ 注意：这里的 func 不再是 search.run，而是我们自定义的包装函数
        func=proxied_google_search,
        description="当需要回答有关时事、最新信息或不确定的事实性问题时，应使用此工具进行网络搜索。"
    ),
    # 新增的计算器工具
    Tool(
        name="Calculator",
        # 注意这里的 func 是 llm_math_chain.run
        # 它专门接收并解决数学表达式问题
        func=llm_math_chain.run,
        description="当你需要进行精确的数学计算或解决数学问题时使用此工具。输入应该是一个完整的数学问题。"
    )
]

# 调用测试
from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) 

print("--- 案例1: 触发搜索引擎 ---")
response1 = agent_executor.invoke({"input": "Kimi AI 是哪个公司开发的？"})
print("\n[最终答案]:", response1['output'])

print("\n" + "="*50 + "\n")

print("--- 案例2: 触发计算器 ---")
# 这个问题 LLM 自己算很容易错，所以它应该选择 Calculator 工具
response2 = agent_executor.invoke({"input": "如果一个圆的半径是 5.8 厘米，它的面积是多少平方厘米？请使用 π=3.14159。"})
print("\n[最终答案]:", response2['output'])

# 因为没有设置memory，所以主体信息是缺失的，不能满足对话场景的要求。
# 那下节课，就跟agent加上memory，让前后文有一个承接关系。
response1 = agent_executor.invoke({"input": "百日咳是一种什么病？"})
print("\n[最终答案]:", response1['output'])
response2 = agent_executor.invoke({"input": "吃什么药好得快？"})
print("\n[最终答案]:", response2['output'])