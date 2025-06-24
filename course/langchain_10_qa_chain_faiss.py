# 上节课已经搞定了基于文本的问答逻辑，但是遗留了一个问题，就是不管文本和问题有没有关系，我们都会传给了大模型进行分析。
# 这样处理有两个问题，一个是费钱，有很多废话也会占用token，另一方面，会对模型做判断有干扰。属于费钱不讨好。
# 所以我们的方案是先做过滤，也叫召回，然后只把相关文本传给大模型。
# 召回的过程我们需要用到一个三方的相似性搜索库，叫做FAlSS。
# Faiss是Facebook Al Similarity Search的缩写，是Facebook Al团队开源的针对聚类和相似性搜索库。

from langchain.schema import Document
corpus = [
    '武汉市，简称“汉”，别称江城，湖北省辖地级市、省会，副省级市、国家中心城市、超大城市，国务院批复确定的中国中部地区的中心城市。',
    '武汉市下辖13个区，总面积8569.15平方千米。截至2022年末，常住人口1373.90万人，地区生产总值18866.43亿元。',
    '武汉市地处江汉平原东部、长江中游，长江及其最大支流汉水在此交汇，形成武汉三镇（武昌、汉口、汉阳）隔江鼎立的格局。',
    '湖北省，简称“鄂”，别名楚、荆楚，中华人民共和国省级行政区，省会武汉。',
    '截至2022年末，湖北省常住人口5844万人，地区生产总值为53734.92亿元，人均地区生产总值为92059元。', 
    '湖北省辖12个地级市、1个自治州，39个市辖区、26个县级市、37个县（其中2个自治县）、1个林区。']
documents = [Document(page_content=cp) for cp in corpus]

# 1.安装
# pip install faiss-cpu

# 2.文档向量化
from langchain.vectorstores.faiss import FAISS

# from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

# embedding = OpenAIEmbeddings(model = 'text-embedding-ada-002')
model_name = "shibing624/text2vec-base-chinese"
embedding = HuggingFaceEmbeddings(model_name=model_name)

documents_db = FAISS.from_documents(documents, embedding)

print(documents_db)

# 3.文档过滤，召回最相关的3条
question = '武汉三镇是哪三个？'
# question = '湖北省常住人口是多少？'
retrieval_documents = documents_db.similarity_search(query=question, k=3)
print(retrieval_documents)
# exit()

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="moonshot-v1-8k")

from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(llm=llm, chain_type = 'stuff', verbose = True)
result = chain.run(input_documents = retrieval_documents, question = question)
print(result)

# 4.召回方法
# 相似性搜索，只返回最相关的k条数据
documents_db.similarity_search(query = question, k = 3)
# 相似性搜索，并返回相似度分数，分数越小越相关
documents_db.similarity_search_with_score(query = question, k = 3)
# 相似性搜索，分数越大越相关
documents_db.similarity_search_with_relevance_scores(query = question, k = 3)
# 最大边际搜索，优化了与查询的相似性和文档之间的多样性
documents_db.max_marginal_relevance_search(query = question, k = 3)

# 另外，还有Milvus、Pinecone等向量数据库都可以实现相似性搜索的功能。这些库LangCHain都做了集成，感兴趣的可以自己研究，用法上都是类似的。