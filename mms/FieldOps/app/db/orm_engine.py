from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# 连接字符串（使用 SQLite，未来可替换为 PostgreSQL/MySQL）
SQLALCHEMY_DATABASE_URL = "sqlite:///./fieldops.db"

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 特性，仅在多线程时需要
)

# 基类（所有模型继承此基类）
Base = declarative_base()
