# mms/FieldOps/router.py

from fastapi import APIRouter
from .api.location_api import location_router
from .api.batch_api import task1_batch_router

class FieldOpsRouter:
    def __init__(self):
        self.router = APIRouter()
        self._merge_all_routers()

    def _merge_all_routers(self):
        """
        合并所有模块的路由：
        - /FieldOps/api/tree → 位置结构树（来自 location_router）
        - /FieldOps/api/events → 事件流（待实现）
        - /FieldOps/api/batches → 批次列表（待实现）
        - /FieldOps/{batch_id} → 批次详情（来自 batch_router）
        """
        # 1. 合并位置相关路由（/tree, /barn/{barn_id}/pens）
        self.router.include_router(location_router, prefix="/api", tags=["location"])
        
        # 2. 合并批次相关路由（/{batch_id}, /{batch_id}/distribute, /{batch_id}/event）
        self.router.include_router(task1_batch_router, prefix="/api", tags=["batch"])
        
        # 3. 可扩展：添加 /api/events, /api/batches 等接口（后续实现）
        
# 实例化并导出路由
task1_router = FieldOpsRouter().router