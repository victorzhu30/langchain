# 在前面课程当中，我们基本已经学完了LangChain的重要知识点，为了给后面的项目减负，提前给大家讲两个项目中的细节。
# 这节课先讲第一个，就是用大模型做命名实体识别，主要涉及的知识点是格式化输出。

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="moonshot-v1-8k", 
                openai_api_base="https://api-sg.moonshot.ai/v1/",
                temperature=0)

# ResponseSchema用来定义“模板”中的每一个字段（每一行）。
# StructuredOutputParser用来创建和管理整个“模板”。
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# 定义实体字段
# 做命名实体识别的目的是要把实体提取出来填充CQL模型的，所以我们希望大模型处理完之后的数据就是一个字典数据。
# 这个过程需要用到LangChain中的格式化输出。

# 类型：list, string, number
response_schema = [
    ResponseSchema(type='list', name='disease', description='疾病名称实体'),
    ResponseSchema(type='list', name='symptom', description='疾病症状实体'),
    ResponseSchema(type='list', name='drug', description='药物名称实体'),
] 
# 使用上面定义的模板来创建一个“结构化输出解析器”
output_parser = StructuredOutputParser.from_response_schemas(response_schema)
# 从解析器中获取自动生成的、给大模型的“格式说明书”
format_instructions = output_parser.get_format_instructions()
# print(format_instructions) # 这会打印出一段文本，告诉大模型应该如何格式化它的回答

# 定义提示词模板
# 考虑到大模型可能会生成文本中没有出现过的实体，我们通过自定义提示词的方式让他不要推理。

template = '''
1、从以下用户输入的句子中，提取实体内容。
2、仅根据用户输入抽取，不要推理。
3、注意json格式，在json中不要出现//
4、如果字段内容为空，也需要保留字段名称

{format_instructions}

用户输入：{input}

输出：
'''

from langchain.prompts import PromptTemplate
prompt = PromptTemplate(
    template=template,
    partial_variables={'format_instructions': format_instructions},
    input_variables=['input']
)
# prompt = prompt.format(input='感冒是一种什么病？')
# print(prompt)

# 调用大模型并解析结果
# 因为LangChain预设提示词格式有问题，可能会出现json格式不合法的报错
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# llm_output = chain.run(input='感冒是一种什么病？会导致咳嗽吗？')
llm_output = chain.run(input='感冒吃什么药好得快？可以吃阿莫西林吗？')
print(llm_output)

output = output_parser.parse(llm_output)
print(output, type(output))
# 因为大模型每次生成的内容不完全一样，开发过程中第4步的报错可能出现也有可能不出现。
# 保险起见，下节课还是带大家来重写一下格式化输出的提示词，防止在项目中报错。