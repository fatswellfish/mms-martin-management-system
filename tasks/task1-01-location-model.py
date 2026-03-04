# mms/FieldOps/models/location.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Farm(Base):
    __tablename__ = 'farm'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 一对多关系：一个农场有多个猪舍
    barns = relationship("Barn", back_populates="farm", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Barn(Base):
    __tablename__ = 'barn'

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey('farm.id'), nullable=False)
    name = Column(String(50), nullable=False)
    barn_type = Column(String(20), nullable=False, index=True)  # farrowing, weaning, finishing, etc.
    capacity = Column(Integer, default=30)
    is_reserved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关联到农场
    farm = relationship("Farm", back_populates="barns")

    # 一对多关系：一个猪舍有多个猪栏
    pens = relationship("Pen", back_populates="barn", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "farm_id": self.farm_id,
            "name": self.name,
            "barn_type": self.barn_type,
            "capacity": self.capacity,
            "is_reserved": self.is_reserved,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Pen(Base):
    __tablename__ = 'pen'

    id = Column(Integer, primary_key=True)
    barn_id = Column(Integer, ForeignKey('barn.id'), nullable=False)
    name = Column(String(20), nullable=False)
    capacity = Column(Integer, default=15)
    current_quantity = Column(Integer, default=0)
    is_reserved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 外键关联到猪舍
    barn = relationship("Barn", back_populates="pens")

    # 可选：支持多个批次占用同一栏（通过中间表或外键）
    # 这里暂用 current_quantity 表示当前数量，实际可用 batch_assignments 表

    def to_dict(self):
        return {
            "id": self.id,
            "barn_id": self.barn_id,
            "name": self.name,
            "capacity": self.capacity,
            "current_quantity": self.current_quantity,
            "is_reserved": self.is_reserved,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }