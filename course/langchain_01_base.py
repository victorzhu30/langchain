from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    # openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_base="https://api-sg.moonshot.ai/v1/", 
    openai_api_key="sk-86coYfOVUSazPvNod5hWbx6BCOBZKMHfu2S0RWWwe6QxiVfM",
    model_name="moonshot-v1-8k",
)

print(llm.invoke("how can langsmith help with testing?"))

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="moonshot-v1-8k")

print(llm.invoke("how can langsmith help with testing?"))