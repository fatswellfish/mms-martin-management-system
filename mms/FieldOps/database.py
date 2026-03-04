from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.orm_engine import Base

# 连接字符串（使用 SQLite，未来可替换为 PostgreSQL/MySQL）
SQLALCHEMY_DATABASE_URL = "sqlite:///./fieldops.db"

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 特性，仅在多线程时需要
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据库表（如果不存在）
def init_db():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话的依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
