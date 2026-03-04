from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.orm_engine import Base
from datetime import datetime


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    batch_code = Column(String, unique=True, index=True)  # 例如 20260228，由一次运输进入养殖场
    initial_quantity = Column(Integer, default=0)  # 进场总数量（头）
    current_alive = Column(Integer, default=0)  # 当前存活数量（动态变化）
    total_dead = Column(Integer, default=0)  # 累计死亡数（不包含出栏）
    total_sold_final = Column(Integer, default=0)  # 累计最终出栏数（销售）
    
    # 关联信息：
    parent_batch_id = Column(Integer, nullable=True)  # 如果是子批次（如分栏后产生的新批次）
    source_batch_id = Column(Integer, nullable=True)  # 原始批次来源（如从外部引进）
    
    # 批次状态与生命周期：
    status = Column(String, default="active")  # active, sold, dead, transferred
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键关系：一个批次可以有多个事件（1对多）
    events = relationship("Event", backref="batch", cascade="all, delete-orphan")
    
    # 该批次当前所在的栏位记录（多对多，通过 PigBatchLocation 表关联）
    locations = relationship("PigBatchLocation", backref="batch", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "batch_code": self.batch_code,
            "initial_quantity": self.initial_quantity,
            "current_alive": self.current_alive,
            "total_dead": self.total_dead,
            "total_sold_final": self.total_sold_final,
            "parent_batch_id": self.parent_batch_id,
            "source_batch_id": self.source_batch_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "locations": [loc.to_dict() for loc in self.locations]
        }

    def __repr__(self):
        return f"<Batch(id={self.id}, code='{self.batch_code}', status='{self.status}')>"
