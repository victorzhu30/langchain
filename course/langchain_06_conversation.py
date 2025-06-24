# LangChain作为框架内置了很多特定场景的组合链，如果内置的链能满足业务需求，就不用再自己写了
# ConversationChain是专门用来处理对话场景的

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="moonshot-v1-8k")

# 简单对话场景
# 对话场景最典型的特征就是会有对话历史，当前的这一句话可能是承接之前的对话内容的。

from langchain.chains import ConversationChain

conversation = ConversationChain(llm=llm, verbose=True)
# print(conversation.prompt.template)
while True:
    user_input = input('User: ') 
    result = conversation.invoke({"input": user_input})
    print('Assistant:', result)

# 修改系统提示词
# LangChain中ConversationChain内置的提示词是英文，所以我们用英文打招呼，大模型也会回复英文。
# 修改提示词的目的是希望大模型用中文回答

from langchain.prompts import PromptTemplate

template = '''
下面是一段人类和人工智能之间的友好对话。人工智能是健谈的，并根据其上下文提供许多具体细节如果人工智能不知道一个问题的答案，它就会如实说它不知道。请用中文回复。
    
当前对话:
{history}
User:{input}
Assistant:
'''

prompt =PromptTemplate.from_template(template)
conversation = ConversationChain(llm = llm, prompt = prompt, verbose = True)
# print(conversation.prompt.template)

while True:
    user_input = input('User: ') 
    result = conversation.invoke({"input": user_input})
    print('Assistant:', result)