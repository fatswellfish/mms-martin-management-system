# mms/FieldOps/api/distribute_api.py
# FieldOps 项目 - 分栏分配相关 API 接口（已完成）

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from .batch_model import distribute_batch
from ..database import get_db

router = APIRouter()

@router.post("/batches/{batch_id}/distribute")
async def distribute_batch_route(
    batch_id: str,
    distribution_map: dict = Body(...),
    db: Session = Depends(get_db)
):
    """执行分栏逻辑，支持多舍多栏分配"""
    try:
        success = distribute_batch(db, batch_id, distribution_map)
        if not success:
            raise HTTPException(status_code=500, detail="Distribution failed")
        return {"success": True, "message": "Batch distributed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")