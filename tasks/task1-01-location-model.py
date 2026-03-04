# mms/FieldOps/models/location.py
# FieldOps 项目 - 位置体系核心模型（已完成）

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Farm(Base):
    __tablename__ = 'farms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    location = Column(String(255))  # 地理位置坐标或地址
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 与猪舍的关联关系（一对多）
    barns = relationship("Barn", back_populates="farm", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Barn(Base):
    __tablename__ = 'barns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # "Sow", "Farrowing", "Gestation", "Finishing"
    capacity = Column(Integer, nullable=False)  # 最大容纳数量
    reserved_count = Column(Integer, default=0)  # 已预留数量（用于动态分配）
    farm_id = Column(Integer, ForeignKey('farms.id'), nullable=False)
    
    # 外键关联到农场
    farm = relationship("Farm", back_populates="barns")
    
    # 与猪栏的关联关系（一对多）
    pens = relationship("Pen", back_populates="barn", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capacity": self.capacity,
            "reserved_count": self.reserved_count,
            "farm_id": self.farm_id,
            "created_at": self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            "updated_at": self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }


class Pen(Base):
    __tablename__ = 'pens'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), default="empty")  # "empty", "occupied", "reserved", "maintenance"
    current_batch_id = Column(Integer, nullable=True)  # 当前占用批次的ID
    capacity = Column(Integer, nullable=False)  # 栏位容量（头数）
    barn_id = Column(Integer, ForeignKey('barns.id'), nullable=False)
    
    # 外键关联到猪舍
    barn = relationship("Barn", back_populates="pens")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "current_batch_id": self.current_batch_id,
            "capacity": self.capacity,
            "barn_id": self.barn_id,
            "created_at": self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            "updated_at": self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }

# --- 附加：查询辅助函数 ---

def get_farm_tree(session):
    """返回完整的农场结构树，包含所有层级数据"""
    farms = session.query(Farm).all()
    tree = []
    for farm in farms:
        barns = session.query(Barn).filter_by(farm_id=farm.id).all()
        barn_list = []
        for barn in barns:
            pens = session.query(Pen).filter_by(barn_id=barn.id).all()
            pen_list = []
            for pen in pens:
                pen_list.append(pen.to_dict())
            barn_list.append({
                "id": barn.id,
                "name": barn.name,
                "type": barn.type,
                "capacity": barn.capacity,
                "reserved_count": barn.reserved_count,
                "pens": pen_list
            })
        tree.append({
            "id": farm.id,
            "name": farm.name,
            "location": farm.location,
            "barns": barn_list
        })
    return tree


def get_barn_pens(session, barn_id):
    """获取某猪舍的所有栏位及占用情况"""
    barn = session.query(Barn).filter_by(id=barn_id).first()
    if not barn:
        return None
    pens = session.query(Pen).filter_by(barn_id=barn_id).all()
    return [pen.to_dict() for pen in pens]