from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Farm(Base):
    __tablename__ = 'farms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    # 一对多关系：一个农场有多个猪舍
    barns = relationship("Barn", back_populates="farm")

class Barn(Base):
    __tablename__ = 'barns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # "fattening", "parturition", etc.
    farm_id = Column(Integer, ForeignKey('farms.id'))
    
    # 外键关联到农场
    farm = relationship("Farm", back_populates="barns")
    
    # 一对多关系：一个猪舍有多个猪栏
    pens = relationship("Pen", back_populates="barn")

class Pen(Base):
    __tablename__ = 'pens'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    reserved = Column(Boolean, default=False)
    barn_id = Column(Integer, ForeignKey('barns.id'))
    
    # 外键关联到猪舍
    barn = relationship("Barn", back_populates="pens")