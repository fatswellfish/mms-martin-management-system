# mms/FieldOps/migrations/batch_migration.py
# FieldOps 项目 - 批次与事件数据库迁移脚本（已完成）

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
import datetime

# 连接数据库（假设使用 SQLite，路径为 ./data/fieldops.db）
db_url = "sqlite:///./data/fieldops.db"
engine = create_engine(db_url)
metadata = MetaData()

# 定义表结构（与 models/batch.py 一致）

def create_tables():
    # Batch 表
    batches_table = Table(
        'batches', metadata,
        Column('id', Integer, primary_key=True),
        Column('batch_id', String(50), nullable=False, unique=True),
        Column('quantity', Integer, nullable=False),
        Column('status', String(20), default="active"),
        Column('created_at', DateTime, default=datetime.datetime.utcnow),
        Column('updated_at', DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    )
    
    # Event 表
    events_table = Table(
        'events', metadata,
        Column('id', Integer, primary_key=True),
        Column('event_type', String(50), nullable=False),
        Column('timestamp', DateTime, default=datetime.datetime.utcnow),
        Column('batch_id', Integer, ForeignKey('batches.id'), nullable=True),
        Column('pen_id', Integer, ForeignKey('pens.id'), nullable=True),
        Column('barn_id', Integer, ForeignKey('barns.id'), nullable=True),
        Column('description', String(500))
    )
    
    # 批次与栏位关联表（多对多）
    batch_pen_association = Table(
        'batch_pen', metadata,
        Column('batch_id', Integer, ForeignKey('batches.id'), primary_key=True),
        Column('pen_id', Integer, ForeignKey('pens.id'), primary_key=True)
    )
    
    # 创建所有表
    try:
        metadata.create_all(engine)
        print("✅ 批次与事件体系数据库表已成功创建")
    except Exception as e:
        print(f"❌ 数据库创建失败: {e}")

if __name__ == "__main__":
    create_tables()