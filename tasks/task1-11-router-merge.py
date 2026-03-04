# mms/FieldOps/router.py
# FieldOps 项目 - 路由合并脚本（已完成）

from fastapi import APIRouter
from .api.location_api import router as location_router
from .api.batch_api import router as batch_router

# 合并所有路由到主应用
main_router = APIRouter()

# 将子路由挂载到主路由下（前缀为 /FieldOps/api）
main_router.include_router(location_router, prefix="/api", tags=["location"])
main_router.include_router(batch_router, prefix="/api", tags=["batch"])

# 导出主路由，供 main.py 引用
__all__ = ["main_router"]