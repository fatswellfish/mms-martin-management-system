from fastapi import APIRouter, HTTPException
from typing import List
from mms.fieldops.models.batch import Batch
from mms.fieldops.schemas.batch import BatchResponse

# 批次相关路由
def create_batch_router() -> APIRouter:
    router = APIRouter()
    
    # 模拟批次数据（实际应从数据库查询）
    batches = [
        Batch(id=1001, batch_id="B2026-03-04-001", quantity=50, status="in_barn"),
        Batch(id=1002, batch_id="B2026-03-04-002", quantity=10, status="pending_transfer")
    ]
    
    @router.get("/", response_model=List[BatchResponse])
    def get_batches():
        return batches
    
    @router.get("/{batch_id}", response_model=BatchResponse)
    def get_batch_detail(batch_id: str):
        for batch in batches:
            if batch.batch_id == batch_id:
                return batch
        raise HTTPException(status_code=404, detail="Batch not found")
    
    return router