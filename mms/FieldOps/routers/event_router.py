from fastapi import APIRouter, HTTPException
from typing import List
from mms.FieldOps.models.event import Event
from mms.FieldOps.schemas.event import EventResponse

# 事件相关路由
def create_event_router() -> APIRouter:
    router = APIRouter()
    
    # 模拟事件数据（实际应从数据库查询）
    events = [
        Event(id=1, event_type="transfer", timestamp="2026-03-04T18:30:00", batch_id="B2026-03-04-001", pen_id=1001, description="从育肥舍转至产房"),
        Event(id=2, event_type="death", timestamp="2026-03-04T17:15:00", batch_id="B2026-03-04-002", pen_id=1003, description="1头猪死亡")
    ]
    
    @router.get("/", response_model=List[EventResponse])
    def get_events():
        return events
    
    return router