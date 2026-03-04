# mms/FieldOps/api/batches_api.py
# FieldOps 项目 - 批次列表相关 API 接口（已完成）

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .batch_model import get_batch_detail
from ..database import get_db

router = APIRouter()

@router.get("/batches")
async def get_batch_list(
    db: Session = Depends(get_db),
    status: str = Query(None, description="过滤状态: active, transferring, finished, dead")
):
    """获取批次列表，支持按状态筛选"""
    try:
        # 构建查询条件
        query = db.query(Batch)
        
        if status:
            query = query.filter(Batch.status == status)
        
        # 获取所有批次（按创建时间倒序）
        batches = query.order_by(Batch.created_at.desc()).all()
        
        # 转换为字典列表（供前端使用）
        batch_list = [batch.to_dict() for batch in batches]
        
        return {
            "success": True,
            "data": batch_list,
            "total": len(batch_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")