# mms/fieldops/routers/router.py
from fastapi import APIRouter
from starlette.responses import FileResponse
import os

router = APIRouter()

# 1. 根路由，返回主页内容（静态文件）
@router.get("/")
def get_index():
    # 指向 index.html 文件的路径。
    file_path = "mms/fieldops/index.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "index.html not found"}

# 2. 用于提供前端页面的路由（如果存在）
@router.get("/index.html")
def get_index_html():
    file_path = "mms/fieldops/index.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "index.html not found"}