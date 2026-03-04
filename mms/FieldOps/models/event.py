from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String(50), nullable=False)  # "transfer", "death", "sale", "vaccination", etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    batch_id = Column(String(50), ForeignKey('batches.batch_id'))
    pen_id = Column(Integer, ForeignKey('pens.id'))
    barn_id = Column(Integer, ForeignKey('barns.id'))
    description = Column(String(200))
    
    # 外键关联
    batch = relationship("Batch")
    pen = relationship("Pen")
    barn = relationship("Barn")