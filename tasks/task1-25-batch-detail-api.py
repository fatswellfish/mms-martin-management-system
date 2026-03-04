# mms/FieldOps/api/batch_detail_api.py
# FieldOps 项目 - 批次详情相关 API 接口（已完成）

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .batch_model import get_batch_detail
from ..database import get_db

router = APIRouter()

@router.get("/batches/{batch_id}")
async def get_batch_detail_route(batch_id: str, db: Session = Depends(get_db)):
    """获取批次详情，包含事件历史和分配的栏位"""
    try:
        detail = get_batch_detail(db, batch_id)
        if not detail:
            raise HTTPException(status_code=404, detail="Batch not found")
        return {"success": True, "data": detail}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")