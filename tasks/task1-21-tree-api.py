# mms/FieldOps/api/tree_api.py
# FieldOps 项目 - 农场结构树相关 API 接口（已完成）

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .location_model import get_farm_tree
from ..database import get_db

router = APIRouter()

@router.get("/tree")
async def get_farm_structure(db: Session = Depends(get_db)):
    """返回完整的农场结构树，用于前端渲染"""
    try:
        tree = get_farm_tree(db)
        return {"success": True, "data": tree}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")