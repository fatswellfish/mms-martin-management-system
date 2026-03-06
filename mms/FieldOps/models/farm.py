from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Farm(Base):
    __tablename__ = 'farms'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, id=None, name=None, location=None, created_at=None):
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if location is not None:
            self.location = location
        if created_at is not None:
            self.created_at = created_at