# api/routers/data_router.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# 🔌 引入我们刚刚打造的数据库引擎和表结构
from mock_db.database import SessionLocal, SleepRecord 

router = APIRouter()

# 🛡️ Pydantic 模型：海关安检员。严格校验前端发来的 JSON 长什么样
class SleepDataPayload(BaseModel):
    user_id: str
    heart_rate: int
    hrv: int
    movement: int

# ⚙️ 核心机制：数据库连接池 (Dependency Injection)
# 每次前端发来请求，它就去工厂拿一个连接；请求处理完，自动归还连接，绝不内存泄漏。
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚀 接收前端数据的 API 接口
@router.post("/")
def receive_ring_data(payload: SleepDataPayload, db: Session = Depends(get_db)):
    print(f"[数据总线] 接收到 {payload.user_id} 的数据，准备物理落盘...")

    # 🧠 模拟极其简单的服务端算法：根据体动和心率，算出一个睡眠得分
    # 假设：心率越接近 60 越好，体动越少越好
    calculated_score = 100 - payload.movement - abs(payload.heart_rate - 60)
    final_score = max(0, min(100, calculated_score)) # 把分数限制在 0-100 之间

    # 📦 ORM 魔法：把 Python 的数据，塞进我们刚才画好的表结构 (SleepRecord) 里
    db_record = SleepRecord(
        user_id=payload.user_id,
        heart_rate=payload.heart_rate,
        hrv=payload.hrv,
        movement=payload.movement,
        sleep_score=final_score
    )

    # 💾 物理落盘三部曲 (绝不能少)
    db.add(db_record)        # 1. 放到暂存区
    db.commit()              # 2. 敲下回车，物理写入硬盘 (Transaction Commit)
    db.refresh(db_record)    # 3. 重新读取硬盘，拿到数据库自动生成的绝对唯一 ID

    print(f"[数据总线] 落盘成功！数据库分配的主键 ID: {db_record.id}, 计算得分: {final_score}")

    # 给前端返回极其专业的回执
    return {
        "status": "success", 
        "message": f"Data persisted! DB Record ID: {db_record.id}, Score: {final_score}"
    }