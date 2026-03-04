from fastapi import APIRouter

# 导入所有子路由
from .batch_router import router as batch_router
from .event_router import router as event_router
from .experiment_router import router as experiment_router
from .tree_router import router as tree_router
from .barn_router import router as barn_router
from .pen_router import router as pen_router

# 合并所有路由
api_router = APIRouter()
api_router.include_router(batch_router)
api_router.include_router(event_router)
api_router.include_router(experiment_router)
api_router.include_router(tree_router)
api_router.include_router(barn_router)
api_router.include_router(pen_router)

__all__ = ["api_router"]
