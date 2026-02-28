写入文件 mms/FieldOps/main.py；
内容为：
from fastapi import FastAPI
from .router import router as fieldops_router
from .router_views import router as views_router

app = FastAPI(title="FieldOps")
app.include_router(fieldops_router)
app.include_router(views_router)
