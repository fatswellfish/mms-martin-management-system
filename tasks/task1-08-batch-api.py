# mms/FieldOps/api/batch_api.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .database import get_db
from .services.batch_service import get_batch_detail, distribute_batch_to_pens, create_event
from typing import List, Dict, Optional

class BatchAPI:
    def __init__(self):
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        """
        设置所有与批次相关的后端接口路由。
        """
        # 1. 获取批次详情（用于前端卡片展示）
        @self.router.get("/{batch_id}", tags=["batch"])
        def get_batch_detail_endpoint(batch_id: str):
            db = next(get_db())
            result = get_batch_detail(db, batch_id)
            if not result["success"]:
                raise HTTPException(status_code=404, detail=result["error"])
            return result["data"]

        # 2. 批次分栏接口（用于事件驱动）
        @self.router.post("/{batch_id}/distribute", tags=["batch"])
        def distribute_batch_endpoint(batch_id: str, distribution_map: Dict[str, int]):
            db = next(get_db())
            result = distribute_batch_to_pens(db, batch_id, distribution_map)
            if not result["success"]:
                raise HTTPException(status_code=400, detail=result["error"])
            return result

        # 3. 创建新事件接口（用于系统日志记录）
        @self.router.post("/{batch_id}/event", tags=["batch"])
        def create_event_endpoint(
            batch_id: str,
            event_type: str = Query(...),
            pen_id: int = None,
            barn_id: int = None,
            description: str = None
        ):
            db = next(get_db())
            result = create_event(db, event_type, batch_id, pen_id, barn_id, description)
            if not result["success"]:
                raise HTTPException(status_code=400, detail=result["error"])
            return result["data"]

# 实例化并导出路由
task1_batch_router = BatchAPI().router