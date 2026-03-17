from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
import uvicorn

# 1. 实例化核心路由节点
app = FastAPI(title="Smart Ring MVP", version="1.0.0")

# 2. 配置跨域 (CORS) - 极其重要，否则你的前端网页调不通这个接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # MVP 阶段允许所有前端来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 极简健康检查接口
@app.get("/health")
def health_check():
    return {"status": "System Online", "component": "FastAPI Gateway"}

# 4. 为云端部署预留的 AWS Lambda 适配器接口
# 本地运行 uvicorn 时不会用到它，但上云时极其关键
handler = Mangum(app)

if __name__ == "__main__":
    # 仅供本地调试使用
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)