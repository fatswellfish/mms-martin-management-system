# mms/fieldops/routers/__init__.py
# 用于导出模块的公共接口，例如 router，供主应用加载。
from .router import router
from .main_router import create_main_router

# 导出主路由实例
router = create_main_router()

__all__ = ['router']