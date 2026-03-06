from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime

class Base:
    pass

class Batch(Base):
    __tablename__ = 'batches'

    id = Column(Integer, primary_key=True)
    batch_id = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, id=None, batch_id=None, quantity=None, status=None, timestamp=None):
        if id is not None:
            self.id = id
        if batch_id is not None:
            self.batch_id = batch_id
        if quantity is not None:
            self.quantity = quantity
        if status is not None:
            self.status = status
        if timestamp is not None:
            self.timestamp = timestamp

class Transfer(Base):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)