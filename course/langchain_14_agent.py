# 前面课程中给大家讲解了一些常用的chain。这节课开始介绍langchain中另一个重要的概念，叫做agent。
# agent的核心思想是使用大语言模型（LLM）作为推理的大脑，以制定解决问题的计划，借助工具实施动作。

# 尝试做一个数学计算：LLM本质上是文本补全的过程，计算能力是比较差的
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="moonshot-v1-8k")

# 直接调用模型，结果错误
# print(llm.invoke('3.14^6.5')) # 1698.41

# 内置agent
# 大模型无法主动更新自己的知识，所以需要一些外部工具来加强大模型的能力

# pip install numexpr
from langchain.agents import load_tools, initialize_agent, get_all_tool_names
print(get_all_tool_names())
# ['sleep', 'wolfram-alpha', 'google-search', 'google-search-results-json', 'searx-search-results-json', 
#  'bing-search', 'metaphor-search', 'ddg-search', 'google-books', 'google-lens', 'google-serper', 
#  'google-scholar', 'google-finance', 'google-trends', 'google-jobs', 'google-serper-results-json', 
#  'searchapi', 'searchapi-results-json', 'serpapi', 'dalle-image-generator', 'twilio', 'searx-search', 
#  'merriam-webster', 'wikipedia', 'arxiv', 'golden-query', 'pubmed', 'human', 'awslambda', 'stackexchange', 
#  'sceneXplain', 'graphql', 'openweathermap-api', 'dataforseo-api-search', 'dataforseo-api-search-json', 
#  'eleven_labs_text2speech', 'google_cloud_texttospeech', 'read_file', 'reddit_search', 'news-api', 
#  'tmdb-api', 'podcast-api', 'memorize', 'llm-math', 'open-meteo-api', 'requests', 'requests_get', 
#  'requests_post', 'requests_patch', 'requests_put', 'requests_delete', 'terminal']

# tools = load_tools(['llm-math'], llm = llm)
# agent = initialize_agent(tools, llm = llm)
# print(agent.run('请计算3.14的6.5次方'))
# 详见langchain_14_agentv2.py

# 自定义工具
# 内置工具不能满足业务需求，需要结合业务场景来自定义工具
from datetime import datetime
from langchain.tools import Tool

def get_current_time(query):
    return datetime.now()

tools = [Tool(
    name='get_current_time',
    func=get_current_time,
    description='获取当前日期时间'
)]

agent = initialize_agent(tools, llm=llm, verbose=True)
result = agent.run('今天是几号？')
print(result)
# 通过以上概念，相信大家对agent的概念有了进一步的理解。通俗解释，agent就是将模型进行封装，使得它可以通过用户的输入理解用户的意图，然后执行一个特定的动作。
