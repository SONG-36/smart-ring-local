# mock_db/database.py
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# ==========================================
# 1. 物理寻址：告诉系统，数据库文件存在哪里？
# 这里的 sqlite:///./ring_data.db 意味着：在你的项目根目录下，生成一个名为 ring_data.db 的文件。
# ==========================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./ring_data.db"

# ==========================================
# 2. 点火：启动数据库引擎 (Engine)
# check_same_thread=False 是 SQLite 在多线程 Web 环境下的防弹设置
# ==========================================
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ==========================================
# 3. 建立连接池：创建一个制造“数据库对话 (Session)”的工厂
# ==========================================
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 声明所有数据表的“祖先基类”
Base = declarative_base()

# ==========================================
# 5. 定义表结构 (Schema)：这才是真正决定你的数据在硬盘上长什么样的骨架！
# ==========================================
class SleepRecord(Base):
    __tablename__ = "sleep_records" # 在数据库里，这张表叫这个名字

    # 定义列 (Columns)：这里就是未来存放你戒指数据的格子
    id = Column(Integer, primary_key=True, index=True) # 每一行数据的绝对唯一身份证
    user_id = Column(String, index=True)               # 用户 ID (比如 user_123)
    heart_rate = Column(Integer)                       # 心率
    hrv = Column(Integer)                              # 心率变异性
    movement = Column(Integer)                         # 体动次数
    sleep_score = Column(Integer)                      # 睡眠综合得分

# ==========================================
# 6. 一键建表脚本 (手术刀)
# 当你直接运行这个文件时，它会拿着上面的图纸，去你的硬盘上物理开凿出这个数据库。
# ==========================================
if __name__ == "__main__":
    print("🛠️ 正在初始化物理数据库...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表已在硬盘上物理创建成功！")