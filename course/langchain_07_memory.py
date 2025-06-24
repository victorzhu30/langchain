# 前面课程中学习了内置的对话场景处理链叫做ConversationChain。
# 直观上感觉，这种方法还不如直接调OpenAI接口方便，而且之前提到的越聊越贵的问题，好像也没有解决，还是会把全部对话信息都带过去。
# 其实对于这个问题，LangChain是有处理方案的，这节课我们一起来学习一个新的概念叫做Memory，用它就能比较好的解决对话记忆的问题。

import time

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="moonshot-v1-8k")

from langchain.chains import ConversationChain

# 只保留两轮history
from langchain.memory import ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=2)

conversation = ConversationChain(llm = llm, memory =  memory, verbose = True)

result = conversation.invoke({'input': 'hello'})
result = conversation.invoke({'input': '你叫什么名字？'})
result = conversation.invoke({'input': '感冒是一种什么病？'})
time.sleep(60)
result = conversation.invoke({'input': '一般会有哪些症状？'})
result = conversation.invoke({'input': '吃什么药好得快？'})
print(result)

#其他常用memory
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory() # 保留完整会话（默认）

from langchain.memory import ConversationSummaryMemory
memory = ConversationSummaryMemory(llm = llm) # 总结前面的对话内容
conversation = ConversationChain(llm = llm, memory =  memory, verbose = True)

result = conversation.invoke({'input': 'hello'})
result = conversation.invoke({'input': '你叫什么名字？'})
time.sleep(60)
result = conversation.invoke({'input': '感冒是一种什么病？'})
print(result)

from langchain.memory import ConversationSummaryBufferMemory 
memory = ConversationSummaryBufferMemory(llm = llm, max_token_limit=100) # 超过最大token数量的会话会被总结