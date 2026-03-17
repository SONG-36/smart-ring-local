# api/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum  # AWS Lambda 适配器

# 引入你的两个业务车间
from api.routers import chat_router, data_router

app = FastAPI(title="Ring API MVP Gateway")

# 🛡️ CORS 跨域防御配置 (允许 Next.js 前端跨端口调用)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 🚦 核心寻址目录 (Router Mounting)
# 这里的 prefix 就是门牌号。前端必须带着这个路径来敲门！
# ==========================================

# 1. 挂载 AI 聊天车间 (前端呼叫 /api/chat 时，引导至此)
app.include_router(chat_router.router, prefix="/api/chat", tags=["AI Coach"])

# 2. 挂载硬件数据接收车间 (前端呼叫 /api/data 时，引导至此)
app.include_router(data_router.router, prefix="/api/data", tags=["Data Ingestion"])

# ==========================================
# 🩺 系统探针 (Health Check)
# ==========================================
@app.get("/health", tags=["0. System Probe"])
def health_check():
    """Lightweight probe for load balancers and container health checks."""
    return {"status": "System Online", "component": "FastAPI Gateway"}

# ==========================================
# ☁️ 云端部署适配器 (AWS Serverless)
# ==========================================
# 将 FastAPI 包装成 AWS Lambda 能识别的格式。
# 这是你未来走向 Remote AWS 开发者的核心桥梁。
handler = Mangum(app)

if __name__ == "__main__":
    # Local development server (仅在本地直接运行 python main.py 时触发)
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)