from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime

class Base:
    pass

class Batch(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Transfer(Base):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)