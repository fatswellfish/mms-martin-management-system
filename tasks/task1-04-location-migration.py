# mms/FieldOps/migrations/location_migration.py
# FieldOps 项目 - 位置体系数据库迁移脚本（已完成）

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
import datetime

# 连接数据库（假设使用 SQLite，路径为 ./data/fieldops.db）
db_url = "sqlite:///./data/fieldops.db"
engine = create_engine(db_url)
metadata = MetaData()

# 定义表结构（与 models/location.py 一致）

def create_tables():
    # Farm 表
    farms_table = Table(
        'farms', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(100), nullable=False, unique=True),
        Column('location', String(255)),
        Column('created_at', DateTime, default=datetime.datetime.utcnow),
        Column('updated_at', DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    )
    
    # Barn 表
    barns_table = Table(
        'barns', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(100), nullable=False),
        Column('type', String(50), nullable=False),
        Column('capacity', Integer, nullable=False),
        Column('reserved_count', Integer, default=0),
        Column('farm_id', Integer, ForeignKey('farms.id'), nullable=False),
        Column('created_at', DateTime, default=datetime.datetime.utcnow),
        Column('updated_at', DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    )
    
    # Pen 表
    pens_table = Table(
        'pens', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(100), nullable=False),
        Column('status', String(20), default="empty"),
        Column('current_batch_id', Integer, nullable=True),
        Column('capacity', Integer, nullable=False),
        Column('barn_id', Integer, ForeignKey('barns.id'), nullable=False),
        Column('created_at', DateTime, default=datetime.datetime.utcnow),
        Column('updated_at', DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    )
    
    # 创建所有表
    try:
        metadata.create_all(engine)
        print("✅ 位置体系数据库表已成功创建")
    except Exception as e:
        print(f"❌ 数据库创建失败: {e}")

if __name__ == "__main__":
    create_tables()