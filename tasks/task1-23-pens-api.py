# mms/FieldOps/api/pens_api.py
# FieldOps 项目 - 猪舍栏位相关 API 接口（已完成）

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .location_model import get_barn_pens
from ..database import get_db

router = APIRouter()

@router.get("/barns/{barn_id}/pens")
async def get_barn_pens(barn_id: int, db: Session = Depends(get_db)):
    """获取某猪舍的所有栏位及占用情况"""
    try:
        pens = get_barn_pens(db, barn_id)
        if not pens:
            raise HTTPException(status_code=404, detail="Barn not found")
        return {"success": True, "data": pens}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")