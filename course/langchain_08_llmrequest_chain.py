# 前面课程中介绍的几种业务Chain虽然场景不同，但都还是在利用，大模型自身的能力回答问题。
# 但有些特定场景，大模型的能力可能是不够的，比如说最新的信息，准确的说是2021年之后的信息。
# 这种情况下最简单的方法就是利用搜索引擎先查询，再用大模型去总结搜索的结果。
# 这个过程LangChain也有内置的链，叫做LLMRequestsChain，我们只需要按照他的格式传参即可，就不需要自己去整理中间数据了。

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="moonshot-v1-8k")

# 定义提示词
from langchain.prompts import PromptTemplate
prompt = PromptTemplate.from_template('''
请根据如下搜索结果，回答用户问题：
搜索结果：
-----------
{requests_result}
-----------
问题：{question}
回答：
'''
)

from langchain.chains import LLMChain, LLMRequestsChain
llm_chain = LLMChain(llm = llm, prompt = prompt, verbose = True)

# 定义请求地址
llm_request_chain = LLMRequestsChain(
    llm_chain = llm_chain,
    verbose = True
)

# question = 'RAG是什么？'
question = '陈华编程是什么？'
inputs = {
    'question': question,
    'url': 'https://www.google.com/search?q=' + question.replace('', '+')
    # 搜索llm-math：https://www.google.com/search?q=llm-math
    # 搜索llm math：https://www.google.com/search?q=llm+math
}

result = llm_request_chain.run(inputs)
print(result)

# 直接爬取Google、百度这类搜索引擎的页面是非常困难且不稳定的。正确的做法是使用它们提供的官方或第三方API。
# 在LangChain中，处理搜索任务的最佳实践是使用 Search API 工具，而不是 LLMRequestsChain。比如使用 SerpApi 或 GoogleSearchAPIWrapper。