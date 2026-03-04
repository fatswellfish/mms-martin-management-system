# mms/FieldOps/models/batch.py
# FieldOps 项目 - 批次与事件核心模型（已完成）

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base
import datetime

# 定义多对多关联表：批次与栏位的关系（支持跨舍移动）
batch_pen_association = Table(
    'batch_pen', Base.metadata,
    Column('batch_id', Integer, ForeignKey('batches.id'), primary_key=True),
    Column('pen_id', Integer, ForeignKey('pens.id'), primary_key=True)
)


class Batch(Base):
    __tablename__ = 'batches'
    
    id = Column(Integer, primary_key=True)
    batch_id = Column(String(50), nullable=False, unique=True)  # 如: B20241201-001
    quantity = Column(Integer, nullable=False)  # 当前批次数量（头数）
    status = Column(String(20), default="active")  # "active", "transferring", "finished", "dead"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 与猪栏的多对多关系（通过关联表）
    pens = relationship("Pen", secondary=batch_pen_association, back_populates="batches")
    
    def to_dict(self):
        return {
            "id": self.id,
            "batch_id": self.batch_id,
            "quantity": self.quantity,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String(50), nullable=False)  # "transfer", "death", "sale", "vaccination", "sick", "treatment"
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    batch_id = Column(Integer, ForeignKey('batches.id'), nullable=True)
    pen_id = Column(Integer, ForeignKey('pens.id'), nullable=True)
    barn_id = Column(Integer, ForeignKey('barns.id'), nullable=True)
    description = Column(String(500))  # 详细说明，如: "因腹泻死亡，数量: 3"
    
    # 外键关联到批次、猪栏、猪舍（可选）
    batch = relationship("Batch", backref="events")
    pen = relationship("Pen", backref="events")
    barn = relationship("Barn", backref="events")
    
    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "batch_id": self.batch_id,
            "pen_id": self.pen_id,
            "barn_id": self.barn_id,
            "description": self.description
        }

# --- 附加：查询辅助函数 ---

def get_batch_detail(session, batch_id):
    """返回批次详情（含分布、事件）"""
    batch = session.query(Batch).filter_by(batch_id=batch_id).first()
    if not batch:
        return None
    
    # 获取所有相关事件（按时间倒序）
    events = session.query(Event).filter_by(batch_id=batch.id).order_by(Event.timestamp.desc()).limit(10).all()
    
    # 获取当前占用的栏位列表（已分配）
    pen_ids = [pen.id for pen in batch.pens]
    
    return {
        "batch": batch.to_dict(),
        "event_history": [event.to_dict() for event in events],
        "assigned_pens": pen_ids
    }


def distribute_batch(session, batch_id, distribution_map):
    """执行分栏逻辑，支持多舍多栏分配"""
    batch = session.query(Batch).filter_by(batch_id=batch_id).first()
    if not batch:
        raise ValueError(f"Batch {batch_id} not found")
    
    # 清除旧的分配关系（避免重复）
    batch.pens.clear()
    
    # 按照 map 进行新分配（格式: {"barn_id": [pen_ids]}
    for barn_id, pen_ids in distribution_map.items():
        barn = session.query(Barn).filter_by(id=barn_id).first()
        if not barn:
            continue
        
        for pen_id in pen_ids:
            pen = session.query(Pen).filter_by(id=pen_id).first()
            if not pen or pen.status != "empty":
                continue
            
            # 将批次加入栏位（并更新状态）
            pen.current_batch_id = batch.id
            pen.status = "occupied"
            batch.pens.append(pen)
    
    session.commit()
    return True