from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pen(Base):
    __tablename__ = 'pens'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    barn_id = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, id=None, name=None, barn_id=None, capacity=None, created_at=None):
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if barn_id is not None:
            self.barn_id = barn_id
        if capacity is not None:
            self.capacity = capacity
        if created_at is not None:
            self.created_at = created_at