写入文件 mms/FieldOps/main.py；
内容为：
from fastapi import FastAPI
from .router import router as fieldops_router
from .router_views import router as fieldops_views_router

app = FastAPI(title="FieldOps")

# 首页级路由
app.include_router(fieldops_router)

# HTML 视图路由
app.include_router(fieldops_views_router)
