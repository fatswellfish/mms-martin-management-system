from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transfer(Base):
    __tablename__ = 'transfers'

    id = Column(Integer, primary_key=True)
    from_pen_id = Column(Integer, nullable=False)
    to_pen_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, id=None, from_pen_id=None, to_pen_id=None, timestamp=None):
        if id is not None:
            self.id = id
        if from_pen_id is not None:
            self.from_pen_id = from_pen_id
        if to_pen_id is not None:
            self.to_pen_id = to_pen_id
        if timestamp is not None:
            self.timestamp = timestamp