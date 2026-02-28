写入文件 mms/FieldOps/router_rewrite.py；
内容为：
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["FieldOps Rewrite"])

# 树结构
@router.get("/pig-farm/tree")
async def _(view: str = None):
    return RedirectResponse(url=f"/FieldOps/farm-tree")

# 结构视图
@router.get("/pig-farm/structure")
async def _():
    return RedirectResponse(url="/FieldOps/farm-structure")

# 批次详情
@router.get("/pig-farm/batch/{batch_id}/tree")
async def _(batch_id: int):
    return RedirectResponse(url=f"/FieldOps/batch-detail?batch_id={batch_id}")

# 默认兜底
@router.get("/pig-farm/{path:path}")
async def _(path: str):
    return RedirectResponse(url="/FieldOps")
    

写入文件 mms/FieldOps/main.py；
内容为：
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .router import router as fieldops_router
from .router_views import router as fieldops_views_router
from .router_rewrite import router as rewrite_router

app = FastAPI(title="FieldOps")

app.mount("/static", StaticFiles(directory="mms/static"), name="static")

app.include_router(rewrite_router)
app.include_router(fieldops_router)
app.include_router(fieldops_views_router)
