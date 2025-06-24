# 前面课程当中还遗留了一个问题，就是需要把向量化之后的数据缓存下来。
# 另外，在真实项目里面可能会有新增文档库的情况。这两个问题这节课一起解决了。

from dotenv import load_dotenv
load_dotenv()

from langchain.document_loaders import PyMuPDFLoader
import os
file_dir = os.path.dirname(__file__)
loader = PyMuPDFLoader(os.path.join(file_dir ,'./data/about.pdf'))

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 50,  # default: 4000
    chunk_overlap = 10  # default: 200
)
documents = loader.load_and_split(text_splitter=text_splitter)

# 存储为本地文件
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
model_name = "shibing624/text2vec-base-chinese"
embedding = HuggingFaceEmbeddings(model_name=model_name)
# documents_db = FAISS.from_documents(documents=documents, embedding=embedding)
# documents_db.save_local('./vector_db')

# 加载本地文件
documents_db = FAISS.load_local('./vector_db', 
                                embeddings=embedding,
                                allow_dangerous_deserialization=True  # <--- 这就是你需要添加的“安全开关”
                                )
# print(documents_db.similarity_search('陈华编程是什么？', k=3))

# 追加数据
print(len(documents_db.docstore._dict))
documents_db_more = FAISS.from_texts(
    ['这是一段需要追加的新文本'],
    embedding=embedding
)
documents_db.merge_from(documents_db_more)
print(len(documents_db.docstore._dict))

# 到现在为止，文档检索问答的功能就全部讲完了。这个功能是比较常用的，而且在后面的综合项目里也会用到。