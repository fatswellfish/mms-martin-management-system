# mms/main.py
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

# 1. 创建主应用实例
app = FastAPI(title="MMS - Main Management System")

# 2. 挂载静态文件目录，用于提供 index.html 等前端资源。
# 这将使得 mms/fieldops/index.html 可以通过 /fieldops/index.html 访问到。
app.mount("/static", StaticFiles(directory="mms/fieldops"), name="static")

# 3. 为模板引擎配置路径（如果需要）
# templates = Jinja2Templates(directory="mms/fieldops")
# app.add_middleware(templates)

# 4. 导入并包含子模块的路由（修正了导入路径）
from .fieldops.routers import main_router
app.include_router(main_router, prefix="/fieldops")

# 5. 根路由 (可选)
@app.get("/")
def read_root():
    return {"message": "Welcome to the MMS homepage. Navigate to /fieldops to access the fieldops module."}