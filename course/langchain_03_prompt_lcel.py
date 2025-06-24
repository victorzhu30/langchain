# 前面的课程中给大家介绍了一个参数的模板定义和传参方法。但有些场景可能需要传多个参数，这节课就来讲解多个参数的模板定义和传参方法。

# 1.多参数Prompt
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model_name="moonshot-v1-8k")
template = '写一首描写{season}的诗，格式要求为{type}'
prompt = PromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt = prompt)
result = chain.invoke({"season": "春天", "type": "五言绝句"})
print(result)

# 2.调用方式
# .run({}), ({}), .invoke({}), .apply({}), .generate({})
# LCEL(LangChainn Expression Language)可以被理解为LangChain的“行话”，是LangChain提供的一种专门的表达式语言。
# 它可以用简洁和灵活的串联语法来定义和操作Chain，使代码更简洁。
chain = prompt | llm
result = chain.invoke({"season": "冬天", "type": "七言律诗"})
print(result)