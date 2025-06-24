# 前面课程中，我们基于文本语料，完成了问答场景的功能，
# 但是用的是文本语料的方式定义的语料库。在实际项目中，文本定义语料库的方式，还是比较少见的，只是方便大家理解。
# 这节课就来介绍几种更常规的格式，比如pdf、csV、txt这些。
# 加载很简单，主要是类似txt这种文本，加载进来之后，还需要做一下分割，比如用txt文件存了一篇小说，不分割就太长了。

import os
file_dir = os.path.dirname(__file__)

# 1.加载CSV文档
from langchain.document_loaders import CSVLoader

loader = CSVLoader(os.path.join(file_dir ,'./data/about.csv'),
                   encoding='utf-8'  # <--- 关键就在这一行！
                   )
# print(loader.load())

# 2.加载其他类型文档
from langchain.document_loaders import TextLoader, PyMuPDFLoader

loader = PyMuPDFLoader(os.path.join(file_dir ,'./data/about.pdf'),
                        # encoding='utf-8'  # <--- 关键就在这一行！
                        )
# print(loader.load())

loader = TextLoader(os.path.join(file_dir ,'./data/about.txt'),
                    encoding='utf-8'  # <--- 关键就在这一行！
                    )
# print(loader.load())

# 3.文件加载和分割
# 分割时需要指定分割的chunk长度和重叠部分的长度。适当的chunk大小和重叠可以提升处理长文本的流畅性和连贯性。
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # separator = ['\n\n', '\n', ' ', ''],
    chunk_size = 50,  # default: 4000
    chunk_overlap = 10  # default: 200
)

documents = loader.load_and_split(text_splitter=text_splitter)
print(len(documents))
print(documents)

# 文件加载并且分割完之后，就跟之前用文本创建的语料结构一样了，一个list包裹多个Document的形式。
# 接下来就可以针对这个文档做问答了。 