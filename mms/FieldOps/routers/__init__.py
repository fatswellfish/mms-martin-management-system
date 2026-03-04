from fastapi import APIRouter
from .api import api_router

# 合并所有路由到主应用
main_router = APIRouter()
main_router.include_router(api_router, prefix="/api")

__all__ = ["main_router"]
