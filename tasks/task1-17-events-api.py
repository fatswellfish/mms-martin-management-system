# mms/FieldOps/api/events_api.py
# FieldOps 项目 - 事件流相关 API 接口（已完成）

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .batch_model import get_batch_detail
from ..database import get_db
import datetime

router = APIRouter()

@router.get("/events")
async def get_event_stream(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """获取事件流，支持分页和滚动加载"""
    try:
        # 从数据库查询事件（按时间倒序）
        events = (
            db.query(Event)
            .order_by(Event.timestamp.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        # 转换为字典列表（供前端使用）
        event_list = [event.to_dict() for event in events]
        
        return {
            "success": True,
            "data": event_list,
            "total": len(event_list),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")