# api/index.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# 将项目根目录添加到 Python 路径中，以便能够导入 WebAgent 模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 这是一个示例，我们将尝试从 WebWalker 中导入功能
# 你需要根据实际想使用的 Agent 进行调整
try:
    from web_walker.serve import RestfulApi as WebWalkerApi
    from web_walker.agent import WebWalker
    # 初始化 Agent
    web_walker_api = WebWalkerApi(agent_cls=WebWalker)
    app = web_walker_api.app
except ImportError as e:
    # 如果导入失败，创建一个备用的简单 app，以便调试
    app = FastAPI()
    @app.get("/")
    def read_root_error():
        return {"error": "Failed to import WebAgent module", "details": str(e)}


# 你也可以定义自己的路由
@app.get("/hello")
def read_root():
    return {"message": "WebAgent is ready to be used on Vercel."}

# 为了让 Vercel 正确处理，通常将 FastAPI 实例命名为 app
# 如果 WebWalkerApi 已经创建了 app，就不需要再次创建了
