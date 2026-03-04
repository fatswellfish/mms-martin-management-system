# mms/FieldOps/api/batch_api.py
# FieldOps 项目 - 批次相关 API 接口（已完成）

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .batch_service import get_batch_detail, distribute_batch
from ..database import get_db

router = APIRouter()

@router.get("/batches/{batch_id}")
async def get_batch_detail(batch_id: str, db: Session = Depends(get_db)):
    """获取批次详情，包含事件历史和分配的栏位"""
    try:
        detail = get_batch_detail(db, batch_id)
        if not detail:
            raise HTTPException(status_code=404, detail="Batch not found")
        return {"success": True, "data": detail}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/batches/{batch_id}/distribute")
async def distribute_batch_route(batch_id: str, distribution_map: dict, db: Session = Depends(get_db)):
    """执行分栏逻辑，支持多舍多栏分配"""
    try:
        success = distribute_batch(db, batch_id, distribution_map)
        if not success:
            raise HTTPException(status_code=500, detail="Distribution failed")
        return {"success": True, "message": "Batch distributed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")