from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.orm_engine import Base


class Pen(Base):
    __tablename__ = "pens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    barn_id = Column(Integer, ForeignKey("barns.id"), nullable=False)
    capacity = Column(Integer, default=0)  # 栏位最大容量（头数）
    is_reserved = Column(Integer, default=0)  # 0: 正常使用，1: 预留（治疗、疗养、留观）
    description = Column(String)

    # 外键关系：一个栏属于一个舍（1对多）
    barn = relationship("Barn", backref="pens")

    # 该栏当前的批次（1对1，可为空）
    current_batch_id = Column(Integer, nullable=True)
    current_quantity = Column(Integer, nullable=True)  # 当前栏中猪的数量（动态变化）

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "barn_id": self.barn_id,
            "barn_name": self.barn.name if self.barn else None,
            "capacity": self.capacity,
            "is_reserved": bool(self.is_reserved),
            "description": self.description,
            "current_batch_id": self.current_batch_id,
            "current_quantity": self.current_quantity
        }

    def __repr__(self):
        return f"<Pen(id={self.id}, name='{self.name}', barn='{self.barn.name}')>"
