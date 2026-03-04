from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mms.FieldOps.models import Base
import os

# 从环境变量读取数据库路径（可选）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///fieldops.db")

# 创建数据库引擎（使用连接池）
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,          # 每次获取连接前检查有效性
    pool_recycle=3600,          # 连接池回收时间（1小时）
    max_overflow=30             # 超出池大小时最多允许的额外连接数
)

# 创建会话工厂（用于数据库操作）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    初始化数据库：创建所有表结构。
    调用此函数后，所有 ORM 模型将被映射为数据库表。
    """
    Base.metadata.create_all(bind=engine)