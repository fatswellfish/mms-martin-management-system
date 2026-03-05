from sqlalchemy import Column, Integer, String
from app.db.orm_engine import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # 产房、保育、育肥、繁育、哺乳、母猪等
    description = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
