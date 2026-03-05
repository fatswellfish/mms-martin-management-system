from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["fieldops Rewrite"])

# 树结构
@router.get("/pig-farm/tree")
async def _(view: str = None):
    return RedirectResponse(url=f"/fieldops/farm-tree")

# 结构视图
@router.get("/pig-farm/structure")
async def _():
    return RedirectResponse(url="/fieldops/farm-structure")

# 批次详情
@router.get("/pig-farm/batch/{batch_id}/tree")
async def _(batch_id: int):
    return RedirectResponse(url=f"/fieldops/batch-detail?batch_id={batch_id}")

# 默认兜底
@router.get("/pig-farm/{path:path}")
async def _(path: str):
    return RedirectResponse(url="/fieldops")
    
