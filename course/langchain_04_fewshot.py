# 举例子
# 在提示词中给几个五言绝句和七言律诗的例子，大模型就能捕捉到格式的信息。
# 用LangChain思路也是一样，只是写法上会略显麻烦，因为它有一层封装

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model="moonshot-v1-8k", temperature=0)

# 定义提示词模板

examples = [{'season': '秋天', 'type': '五言绝句', 'text': '移舟泊烟渚，日暮客愁新。\n野旷天低树，江清月近人。'},
            {'season': '冬天', 'type': '七言律诗', 'text': '昔人已乘黄鹤去，此地空余黄鹤楼。\n黄鹤一去不复返，白云千载空悠悠。\n晴川历历汉阳树，芳草萋萋鹦鹉洲。\n日暮乡关何处是？烟波江上使人愁。'}]

example_template='这是一首描写{season}的诗，格式为{type}: \n{text}'
example_prompt = PromptTemplate.from_template(example_template)

prompt = FewShotPromptTemplate(
    examples=examples,                                  # 前缀
    example_prompt=example_prompt,                      # 传入示例格式化模板
    example_separator="\n\n",                           # 示例之间的分隔符
    prefix='请分析以下诗歌的格式，并按格式要求创作诗歌。',  # 前缀
    suffix='写一首描写{season}的诗，格式要求为{type}:\n', # 后缀，包含最终输入
    input_variables=['season','type']                   # 最终输入的变量名
)

# print(prompt.format(season='秋天', type='七言律诗'))

# 定义LLMChain并调用
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run({'season': '秋天', 'type': '七言律诗'})
print(result)

# 到目前为止，LLMChain的常见用法就讲完了，LLMChain是LangChain中最简单的基础链，虽然它能处理的场景比较简单，但是把多个LLMChain组合起来，就可以实现处理复杂场景的链结构