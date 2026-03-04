# mms/FieldOps/models/batch.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base


class Batch(Base):
    __tablename__ = 'batch'

    id = Column(Integer, primary_key=True)
    batch_id = Column(String(50), unique=True, nullable=False, index=True)  # e.g., "BATCH-2025-04-05-001"
    quantity = Column(Integer, nullable=False, default=600)  # 标准批次大小：600头
    status = Column(Enum('pending', 'in_progress', 'completed', 'transferred', 'out_of_farm'), 
                    nullable=False, default='pending')
    source_pen_id = Column(Integer, ForeignKey('pen.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关联到猪栏（来源）
    source_pen = relationship("Pen", back_populates="batches")

    # 可选：支持多批动物跨舍移动（通过中间表或外键）
    # 这里暂用一个字段表示当前归属栏，实际可用 `current_pens` 表
    current_pens = relationship("Pen", secondary="batch_pen_association", back_populates="batch_assignments")

    def to_dict(self):
        return {
            "id": self.id,
            "batch_id": self.batch_id,
            "quantity": self.quantity,
            "status": self.status,
            "source_pen_id": self.source_pen_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    event_type = Column(Enum('transfer', 'death', 'exit', 'vaccination', 'sick', 'treatment', 'feeding', 'cleaning', 'other'), 
                        nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    batch_id = Column(String(50), nullable=False)  # 引用批次编号（非外键，便于快速查询）
    pen_id = Column(Integer, nullable=True)  # 可选：关联猪栏（用于转栏、死亡等事件）
    barn_id = Column(Integer, nullable=True)  # 可选：关联猪舍（用于转移、防疫等）
    description = Column(String(500), nullable=True)
    is_processed = Column(Boolean, default=False)  # 用于标记是否已处理（如推送通知）

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "batch_id": self.batch_id,
            "pen_id": self.pen_id,
            "barn_id": self.barn_id,
            "description": self.description,
            "is_processed": self.is_processed
        }