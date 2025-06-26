from dotenv import load_dotenv
load_dotenv()

import os
# 检查密钥是否存在
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("GOOGLE_CSE_ID"):
    raise ValueError("请确保在.env文件中设置了GOOGLE_API_KEY和GOOGLE_CSE_ID")

# --- 开始：添加代理设置 ---
# 根据你的v2rayN截图，本地混合代理端口是 10808
# 所以我们使用这个端口
proxy_url = "http://127.0.0.1:10808" 

os.environ["HTTP_PROXY"] = proxy_url
os.environ["HTTPS_PROXY"] = proxy_url
# --- 结束：添加代理设置 ---

from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

tool = Tool(
    name="google_search",
    description="搜索 Google 获取最新结果。",
    func=search.run,
)

print(tool.run("Obama's first name?"))