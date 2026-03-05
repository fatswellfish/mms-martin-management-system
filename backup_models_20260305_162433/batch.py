from sqlalchemy import DateTime
from datetime import datetime

class Base:
    pass

class Transfer(Base):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)