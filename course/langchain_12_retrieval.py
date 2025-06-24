# 前面课程给大家介绍了文档分割和问答的流程，接下来把这两块结合起来，做一个完整的文档检索问答功能。

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="moonshot-v1-8k")

# 加载并分割文档
from langchain.document_loaders import PyMuPDFLoader
import os
file_dir = os.path.dirname(__file__)
loader = PyMuPDFLoader(os.path.join(file_dir ,'./data/about.pdf'),
                        # encoding='utf-8'  # <--- 关键就在这一行！
                        )

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,  # default: 4000
    chunk_overlap = 10  # default: 200
)
documents = loader.load_and_split(text_splitter=text_splitter)
print(len(documents))

# 召回相似片段
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
model_name = "shibing624/text2vec-base-chinese"
embedding = HuggingFaceEmbeddings(model_name=model_name)
documents_db = FAISS.from_documents(documents=documents, embedding=embedding)
question = '陈华编程是什么？'
retrieval_documents = documents_db.similarity_search(query=question, k=3)

# 基于召回片段回答问题
from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(llm=llm, chain_type='stuff', verbose=True)
result = chain.run(input_documents = retrieval_documents, question = question)
print(result)

# 基于文档检索问答的功能就讲完了，但是还存在一个小问题，就是每次提交问题，都需要重新加载文档，然后向量化，这个流程是不太合理的。
# 所以下节课我们讲，把向量化之后的文档缓存下来，这样就不用每次都重新加载了。