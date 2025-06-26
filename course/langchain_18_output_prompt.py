# 1.内置提示词
# The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":
# 
# ```json
# {
#         "disease": list  // 疾病名称实体
#         "symptom": list  // 疾病症状实体
#         "drug": list  // 药物名称实体
# }
# ```

# 2.修改提示词
# 请从以下文本中，抽取出实体信息，并按json格式返回，json包含首尾的“```json”和“```”：
# 以下是字段含义和类型，要求保留所有字段：
# disease 字段，表示：疾病名称实体，类型为：list
# symptom 字段，表示：疾病症状实体，类型为：list
# drug 字段，表示：药物名称实体，类型为：list

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="moonshot-v1-8k", 
                openai_api_base="https://api-sg.moonshot.ai/v1/",
                temperature=0)

from langchain.output_parsers import ResponseSchema, StructuredOutputParser

def structured_output_parser(response_schemas):
    text = '''
请从以下文本中，抽取出实体信息，并按json格式返回，json包含首尾的“```json”和“```”：
以下是字段含义和类型，要求保留所有字段：    
'''
    for schema in response_schemas:
        text += schema.name + ' 字段，表示：'+schema.description + '，类型为：' + schema.type + '\n'
    return text

response_schema = [
    ResponseSchema(type='list', name='disease', description='疾病名称实体'),
    ResponseSchema(type='list', name='symptom', description='疾病症状实体'),
    ResponseSchema(type='list', name='drug', description='药物名称实体'),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = structured_output_parser(response_schemas=response_schema)
# print(format_instructions)

#     请从以下文本中，抽取出实体信息，并按json格式返回，json包含首尾的“```json”和“```”：
#     以下是字段含义和类型，要求保留所有字段：
#     disease 字段，表示：疾病名称实体，类型为：list
# symptom 字段，表示：疾病症状实体，类型为：list
# drug 字段，表示：药物名称实体，类型为：list

# 请从以下文本中，抽取出实体信息，并按json格式返回，json包含首尾的“```json”和“```”：
# 以下是字段含义和类型，要求保留所有字段：
# disease 字段，表示：疾病名称实体，类型为：list
# symptom 字段，表示：疾病症状实体，类型为：list
# drug 字段，表示：药物名称实体，类型为：list

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

from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

llm_output = chain.run(input='感冒是一种什么病？会导致咳嗽吗？')
# llm_output = chain.run(input='感冒吃什么药好得快？可以吃阿莫西林吗？')
print(llm_output)

output = output_parser.parse(llm_output)
print(output, type(output))
