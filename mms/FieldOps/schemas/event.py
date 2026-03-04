from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 事件模型的响应数据结构（用于 API）
class EventResponse(BaseModel):
    id: int
    event_type: str
    timestamp: datetime
    batch_id: str
    pen_id: Optional[int] = None
    barn_id: Optional[int] = None
    description: str