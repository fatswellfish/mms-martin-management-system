from sqlalchemy import Column, Integer, String, DateTime
from app.db.orm_engine import Base
from datetime import datetime

# 事件颜色分类
EVENT_COLOR_MAP = {
    "vaccination": "green",
    "transfer": "blue",
    "illness_mild": "yellow",
    "illness_severe": "red",
    "death": "red",
    "sale": "blue",
    "experiment_1st": "purple",
    "experiment_2nd": "purple",
    "experiment_control": "purple",
    "info": "blue",
}

def get_event_color(event_type: str) -> str:
    return EVENT_COLOR_MAP.get(event_type, "blue")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    event_type = Column(String, index=True)
    level = Column(String, index=True)   # FARM / BARN / PEN / BATCH

    farm_id = Column(Integer, nullable=True)
    barn_id = Column(Integer, nullable=True)
    pen_id = Column(Integer, nullable=True)
    batch_id = Column(Integer, nullable=True)

    quantity = Column(Integer, nullable=True)
    actor = Column(String, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(String)

    severity = Column(String, index=True)
    color = Column(String)  # 用于前端渲染

