from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.orm_engine import Base
from datetime import datetime
from typing import Optional


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)  # transfer, death, sale, vaccination, illness_mild, illness_severe
    level = Column(Enum("FARM", "BARN", "PEN", "BATCH"), index=True)
    farm_id = Column(Integer, nullable=True)
    barn_id = Column(Integer, nullable=True)
    pen_id = Column(Integer, nullable=True)
    batch_id = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)
    actor = Column(String, nullable=True)
    message = Column(String)
    severity = Column(Enum("info", "warning", "error", "critical"), default="info")
    timestamp = Column(DateTime, default=datetime.utcnow)
    color = Column(String, nullable=False)  # 动态生成的颜色，用于卡片展示（如红色=死亡）

    # 外键关系：一个事件属于一个批次（可选）
    batch = relationship("Batch", backref="events")

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "level": self.level,
            "farm_id": self.farm_id,
            "barn_id": self.barn_id,
            "pen_id": self.pen_id,
            "batch_id": self.batch_id,
            "quantity": self.quantity,
            "actor": self.actor,
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
            "color": self.color
        }

    def __repr__(self):
        return f"<Event(id={self.id}, type='{self.event_type}', level='{self.level}')>"


def get_event_color(event_type: str) -> str:
    """根据事件类型返回对应颜色"""
    color_map = {
        "death": "#d32f2f",  # 红色：死亡
        "sale": "#1976d2",   # 蓝色：出栏
        "transfer": "#4caf50", # 绿色：转栏
        "vaccination": "#ff9800", # 橙色：免疫
        "illness_mild": "#ffeb3b", # 黄色：轻病
        "illness_severe": "#f44336", # 深红：重病
        "treatment": "#2196f3", # 浅蓝：治疗
        "other": "#9e9e9e"   # 灰色：其他/默认
    }
    return color_map.get(event_type.lower(), color_map["other"])
