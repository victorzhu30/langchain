# 前面课程当中给大家介绍了 OpenAI 接口实现单轮对话，也就是一问一答的场景。
# 但在真实项目当中，多轮对话也是很常见的，也就是说会有多次提问，并且前后是有承接关系的对话场景。
# 这节课，我们就来用一种简单直接的方式，实现多轮对话的过程。

# 1.基本结构
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

messages = []

# response = client.chat.completions.create(
#     model="moonshot-v1-8k",
#     messages=messages
# )

# print(response.choices[0].message.content)

# 2、循环构建多轮对话
while True:
    content = input('User: ')
    messages.append({"role": "user", "content": content})

    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages
    )

    asst_content = response.choices[0].message.content
    print('Assistant: ', asst_content)
    messages.append({"role": "assistant", "content": asst_content})
    print(messages)

# 3、验证多轮对话效果
# User: 感冒是一种什么病？
# User: 一般会有哪些症状？
# User: 吃什么药好得快？
# 在上面例子中，我们用的是把所有历史对话都带上的方法，实现了多轮对话的效果。
# 但是，大家可能也发现了，这个方法其实存在一个问题就是聊的时间越长会越贵，因为历史的messages会积压，token数量会越来越多。
# 这个问题会在后面Langchain的部分，大家介绍相应的解决方案。