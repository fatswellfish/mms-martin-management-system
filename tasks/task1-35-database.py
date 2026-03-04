# mms/FieldOps/database.py
# FieldOps 项目 - 数据库连接配置（已完成）

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base
import os

# 1. 配置数据库路径（开发环境使用 SQLite，生产环境建议使用 PostgreSQL）
DB_URL = "sqlite:///./data/fieldops.db"

# 2. 为防止并发问题，设置连接池参数（适用于多线程环境）
db_engine = create_engine(
    DB_URL,
    pool_size=20,           # 连接池大小（最大 20 个连接）
    max_overflow=30,        # 超出池大小后最多可创建 30 个额外连接
    pool_pre_ping=True,     # 每次获取连接前检查是否有效（自动重连）
    pool_recycle=3600,      # 每 1 小时回收一次连接（避免长时间闲置连接失效）
    echo=False              # 禁用 SQL 日志输出（生产环境设为 False）
)

# 3. 创建会话工厂（用于创建数据库会话）
SessionLocal = sessionmaker(
    bind=db_engine,
    autocommit=False,       # 不自动提交（需显式 commit）
    autoflush=True          # 自动刷新（在 flush() 时同步到数据库）
)

# 4. 依赖注入函数（FastAPI 使用）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. 公共数据库元数据对象（用于模型映射）
Base = Base

# 6. 初始化数据库表结构（仅在开发环境）
def init_db():
    """在应用启动时创建所有数据库表"""
    Base.metadata.create_all(bind=db_engine)
    print("✅ 所有数据库表已成功创建")

# 7. 连接测试函数（用于调试）
def test_connection():
    """测试数据库连接是否正常"""
    try:
        with db_engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ 数据库连接测试成功")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

# 8. 启动时自动初始化（仅在开发环境）
if __name__ == "__main__":
    # 仅在直接运行此文件时执行初始化（用于测试）
    init_db()
    test_connection()