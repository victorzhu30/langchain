from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="moonshot-v1-8k")

# 构建文档库
from langchain.schema import Document
corpus = [
    '武汉市，简称“汉”，别称江城，湖北省辖地级市、省会，副省级市、国家中心城市、超大城市，国务院批复确定的中国中部地区的中心城市。',
    '武汉市下辖13个区，总面积8569.15平方千米。截至2022年末，常住人口1373.90万人，地区生产总值18866.43亿元。',
    '武汉市地处江汉平原东部、长江中游，长江及其最大支流汉水在此交汇，形成武汉三镇（武昌、汉口、汉阳）隔江鼎立的格局。',
    '湖北省，简称“鄂”，别名楚、荆楚，中华人民共和国省级行政区，省会武汉。',
    '截至2022年末，湖北省常住人口5844万人，地区生产总值为53734.92亿元，人均地区生产总值为92059元。', 
    '湖北省辖12个地级市、1个自治州，39个市辖区、26个县级市、37个县（其中2个自治县）、1个林区。']
documents = [Document(page_content=cp) for cp in corpus]
print(documents)

from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(llm=llm, chain_type = 'stuff', verbose = True)

question = '武汉三镇是哪三个？'
# question = '湖北省常住人口是多少？'
result = chain.run(input_documents = documents, question = question)
print(result)

# chain_type参数

# stuff：将所有文档作为context放入到Prompt中，传递到LLM获取答案，适合小文档。

# refine：上一轮的输出作为下一轮的输入，迭代更新其答案，以获得最好的最终结果。

# map_reduce：将LLM链应用于每个单独的文档，最后合并汇总，得到答案。

# map_rerank：每个文档上运行一个初始提示，再给对应输出给一个分数，返回得分最高的回答。

# 在token数量不超限的情况下，stuff的效果最好。对于简单问答场景，map_rerank也是不错的选择。
# 另外，可以在检索之前对文档内容进行过滤，只保留相关的片段，下节课就来实现这个功能。