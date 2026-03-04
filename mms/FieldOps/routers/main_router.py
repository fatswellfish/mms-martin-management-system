from fastapi import APIRouter
from mms.FieldOps.routers import location_router, batch_router, event_router

# 根路由，用于挂载所有子模块的 API 路由
def create_main_router() -> APIRouter:
    router = APIRouter(prefix="/FieldOps")
    
    # 挂载子路由：位置、批次、事件
    router.include_router(location_router.create_location_router(), prefix="/location")
    router.include_router(batch_router.create_batch_router(), prefix="/batch")
    router.include_router(event_router.create_event_router(), prefix="/event")
    
    return router