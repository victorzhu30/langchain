# 这节课给大家讲解第二个项目细节，针对图数据库的自动问答。
# 所谓的自动，就是不需要人工定义模板，让大模型自动生成Cypher语句，然后查询数据库，得到答案。
# 要用的链是GraphCypherQAChain

# 提前说明一下，目前这种方法在生产项目里面基本上是不可用的，因为他只能处理简单的查询，而且可能会答非所问，所以这节课的内容只需要了解即可。

# 安装扩展
# pip install neo4j
# 使用时：ValueError: Could not use APOC procedures. Please ensure the APOC plugin is installed in Neo4j and that 'apoc.meta.data()' is allowed in Neo4j configuration
# ①拷贝labs/apoc-...-core.jar -> plugins/apoc-...-core.jar
# ②修改conf/neo4j.conf
#   server.directories.plugin=plugins
#   dbms.security.procedures.allowlist=*
#   dbms.security.procedures.unrestricted=*
# ③重启：PS D:\neo4j-community-2025.05.0\bin> .\neo4j.bat restart
# ④验证：return apoc.version()

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="moonshot-v1-8k", 
                openai_api_base="https://api-sg.moonshot.ai/v1/",
                temperature=0)

# 自动问答：利用大模型能力，自动生成Cypher查询语句，执行后得到答案
from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain

graph = Neo4jGraph(
    # url='neo4j://localhost:7687' .env
    username='neo4j',
    password='Zrp031030',
    database='doctor'
)

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True  # <--- 添加这一行
)

result = chain.run('过敏性鼻炎能治好吗？')
print(result)
result = chain.run('鼻炎会有哪些症状？')
print(result)
result = chain.run('感冒是一种什么病？')
print(result)