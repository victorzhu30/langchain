# 上节课当中，我们简单体验了在LangChain框架中调用OpenAI模型的方法
# 接下来，我们介绍提示词模板（PromptTemplate）和一个最基础的Chain（LLMChain）

# 1.提示词模板
# 用模板定义提示词，方便替换变量。比如把春天换成秋天、冬天等
from langchain.prompts import PromptTemplate

template = '写一首描写{season}的诗'

prompt = PromptTemplate(
    template = template,
    input_variables = ['season']
)

print(prompt.format(season='春天'))

# 2.简写形式
prompt = PromptTemplate.from_template(template)
print(prompt.format(season='春天'))

# 3.LLMChain
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model_name="moonshot-v1-8k")

template = '写一首描写{season}的诗'
prompt = PromptTemplate.from_template(template)

chain = LLMChain(llm=llm, prompt = prompt)
result1 = chain.predict(season='冬天')
result2 = chain.invoke({"season": "春天"})
print(result1)
print(result2)

# 上面例子中，只有一个参数，模板定义和传参都比较简单。但有些场景可能会有多个参数。下节课来介绍多个参数的处理方法。