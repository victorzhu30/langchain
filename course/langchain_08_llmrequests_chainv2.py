# pip install bs4 beautifulsoup4
from langchain.chains import LLMRequestsChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# --- 第1步：创建一个用于“处理”网页内容的LLMChain ---

# 定义提示模板，指导LLM如何处理从URL获取的文本
# 注意：这里的input_variables必须包含 'requests_result'，这是LLMRequestsChain固定的输出变量名
# 我们也可以把原始问题'question'传进来，让总结更有针对性
prompt_template = """
根据以下从网站提取的文本，请回答问题：'{question}'
文本内容如下：
---
{requests_result}
---
请根据以上文本，总结并回答问题。
"""

# 创建PromptTemplate对象
prompt = PromptTemplate(
    input_variables=["question", "requests_result"],
    template=prompt_template,
)

# 创建一个LLM实例
llm = ChatOpenAI(model="moonshot-v1-8k", temperature=0)

# 创建一个LLMChain，它的任务是根据提供的文本和问题，生成答案
# 这个chain才是LLMRequestsChain真正需要的“大脑”
processing_chain = LLMChain(llm=llm, prompt=prompt)

# --- 第2步：创建并运行LLMRequestsChain ---

# 创建LLMRequestsChain实例
# 它接收上面创建的processing_chain作为其核心组件
chain = LLMRequestsChain(
    llm_chain=processing_chain,
    # LLMRequestsChain的输入中，除了默认的'url'，其他变量(如此处的'question')会自动传递给内部的llm_chain
    output_key="answer" # 定义最终输出结果的变量名
)

# --- 第3步：执行并查看结果 ---

# 定义我们的问题和我们想查询的URL
user_question = "苹果公司的历史是怎样的？"
# 我们需要手动提供URL
apple_history_url = "https://en.wikipedia.org/wiki/History_of_Apple_Inc."

# 运行链
# 输入是一个字典，key必须包含'url'，这是LLMRequestsChain的默认input_key
# 其他的key（比如'question'）会被传递给内部的processing_chain
result = chain.invoke({
    "url": apple_history_url,
    "question": user_question
})

# 查看最终的答案
print(result["answer"])