from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.orm_engine import Base


class Barn(Base):
    __tablename__ = "barns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description = Column(String)

    # 外键关系：一个舍属于一个类别（产房、保育等）
    category = relationship("Category", backref="barns")

    # 该舍下的所有栏位（1对多）
    pens = relationship("Pen", backref="barn", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,
            "description": self.description
        }

    def __repr__(self):
        return f"<Barn(id={self.id}, name='{self.name}', category='{self.category.name}')>"
