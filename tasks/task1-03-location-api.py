# mms/FieldOps/api/location_api.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .services.location_service import get_farm_tree, get_barn_pens, distribute_batch
from typing import List, Dict, Optional

class LocationAPI:
    def __init__(self):
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        """
        设置所有与位置相关的后端接口路由。
        """
        # 1. 获取农场结构树（用于前端卡片渲染）
        @self.router.get("/tree", tags=["location"])
        def get_farm_structure():
            db = next(get_db())
            result = get_farm_tree(db)
            if not result["success"]:
                raise HTTPException(status_code=500, detail=result["error"])
            return result["data"]

        # 2. 获取指定猪舍的所有栏位信息（用于详情页）
        @self.router.get("/barn/{barn_id}/pens", tags=["location"])
        def get_barn_pens_endpoint(barn_id: int):
            db = next(get_db())
            result = get_barn_pens(db, barn_id)
            if not result["success"]:
                raise HTTPException(status_code=404, detail=result["error"])
            return result["data"]

        # 3. 批次分栏接口（用于事件驱动）
        @self.router.post("/distribute", tags=["location"])
        def distribute_batch_endpoint(batch_id: str, distribution_map: Dict[str, int]):
            db = next(get_db())
            result = distribute_batch(db, batch_id, distribution_map)
            if not result["success"]:
                raise HTTPException(status_code=400, detail=result["error"])
            return result

# 实例化并导出路由
location_router = LocationAPI().router