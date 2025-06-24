# 前面课程中我们花了很大篇幅，介绍了LangChain中的LLMChain这个基础链。基础链一般只用来处理简单问题，但是多个基础链串联起来，就可以解决一些复杂场景的问题了。
# 这节课就来自己写一个顺序链，调两次模型来解决“给公司起名字，并挑选一个最好的”这样一个场景

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# llm = ChatOpenAI(model="moonshot-v1-8k")

# # 第一个Chain
# # 第一次调模型，用于生成一组备选方案

# prompt1 = PromptTemplate.from_template(
#     '有一家公司的创始人叫{name}，主要从事人工智能技术培训和科研辅导，请帮这家公司起5个中文名字，要求包含创始人的名字'
# )

# chain1 = LLMChain(llm = llm, prompt = prompt1, output_key='company_names', verbose = True)
# # print(chain1.invoke({'name': '陈华'}))
# # print(chain1.predict(name='陈华'))
# company_names = chain1.invoke({'name': '陈华'})['company_names']

# # 第二个Chain
# # 第二次调模型，用于从第一个模型生成的结果里面，选出最好的选项

# prompt2 = PromptTemplate.from_template(
#     '请从以下公司名字中，选出你认为最好的一个：\n {company_names}'
# )

# chain2 = LLMChain(llm = llm, prompt = prompt2, verbose = True)
# # print(chain2.predict(company_names=company_names))
# # print(chain2.invoke({'company_names': company_names}))

# # 顺序链
# # 定义SequentialChain顺序链，依次执行前两个Chain
# chain = SequentialChain(chains = [chain1, chain2], input_variables = ['name'], verbose = True)
# print(chain.run({'name': '陈华'}))

# 顺序链的定义就是先定义好子链，然后依次执行即可。
# 需要注意的是，前一个链的结果会作为下一个链的输入，所以上一个链的output_key要和下一个链的入参对上。

# Gemini 2.5 Pro

from langchain.chains import LLMChain, SequentialChain

llm = ChatOpenAI(model="moonshot-v1-8k", temperature=0.7)

# 链1: 生成公司名称
prompt1 = PromptTemplate.from_template(
    "有一家公司的创始人叫{founder_name}，主要从事{business}，请帮这家公司起一个中文名字。"
)
# 注意这里的 output_key
chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="company_name", verbose = True)

# 链2: 写公司简介
prompt2 = PromptTemplate.from_template(
    "请为名为'{company_name}'的公司写一段100字左右的简介。这家公司主要从事{business}。"
)
# 注意这里的 output_key
chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="company_description", verbose = True)

# 使用 SequentialChain 连接
# 它需要知道整个流水线的初始输入和最终输出是什么
seq_chain = SequentialChain(
    chains=[chain1, chain2],
    # 整个流水线的初始输入变量
    input_variables=["founder_name", "business"],
    # 整个流水线最终要返回的输出变量
    # 如果不指定，它会返回所有中间步骤的输出
    output_variables=["company_name", "company_description"],
    verbose=True
)

# 运行整个流水线
# 输入是一个包含所有初始变量的字典
result = seq_chain.invoke({
    "founder_name": "李明",
    "business": "在线少儿编程教育"
})

print("\n--- 最终结果 ---")
print(f"公司名称: {result['company_name']}")
print(f"公司简介: {result['company_description']}")