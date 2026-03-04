from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Batch(Base):
    __tablename__ = 'batches'
    
    id = Column(Integer, primary_key=True)
    batch_id = Column(String(50), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)  # "in_barn", "pending_transfer", etc.
    
    # 多对多关系：一个批次可以分布在多个猪栏中，一个猪栏也可以有多个批次（通过中间表）
    pens = relationship("Pen", secondary="batch_pens", back_populates="batches")

class Transfer(Base):
    __tablename__ = 'transfers'
    
    id = Column(Integer, primary_key=True)
    batch_id = Column(String(50), ForeignKey('batches.batch_id'))
    from_pen_id = Column(Integer, ForeignKey('pens.id'))
    to_pen_id = Column(Integer, ForeignKey('pens.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # 外键关联
    batch = relationship("Batch")
    from_pen = relationship("Pen", foreign_keys=[from_pen_id])
    to_pen = relationship("Pen", foreign_keys=[to_pen_id])