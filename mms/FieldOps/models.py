# mms/fieldops/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Farm(Base):
    __tablename__ = 'farms'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Barn(Base):
    __tablename__ = 'barns'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    farm_id = Column(Integer, ForeignKey('farms.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'farm_id': self.farm_id
        }

class Pen(Base):
    __tablename__ = 'pens'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    barn_id = Column(Integer, ForeignKey('barns.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'barn_id': self.barn_id
        }