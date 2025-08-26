# api/index.py

from fastapi import FastAPI
import sys
import os
import traceback # 引入 traceback 模块

# 将项目根目录添加到 Python 路径中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI()
import_error_details = ""

try:
    # 尝试导入核心模块
    from web_walker.serve import RestfulApi as WebWalkerApi
    from web_walker.agent import WebWalker
    
    # 如果导入成功，则使用真正的 app
    web_walker_api = WebWalkerApi(agent_cls=WebWalker)
    app = web_walker_api.app

except Exception as e:
    # 如果导入失败，捕获详细的错误信息
    # 使用 traceback.format_exc() 获取完整的错误堆栈
    import_error_details = traceback.format_exc()

    # 定义一个显示错误的路由
    @app.get("/")
    def read_root_with_error_details():
        return {
            "status": "ERROR",
            "message": "Failed to initialize WebAgent application.",
            "details": import_error_details
        }

# 添加一个健康的检查点，确保基础 app 在运行
@app.get("/hello")
def read_root():
    return {"message": "WebAgent API endpoint is running, but check root '/' for initialization status."}
