from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .router import router as fieldops_router
from .router_views import router as fieldops_views_router
from .router_rewrite import router as rewrite_router
from .router_events import router as events_router

app = FastAPI(title="FieldOps")

app.mount("/static", StaticFiles(directory="mms/static"), name="static")

app.include_router(events_router)
app.include_router(rewrite_router)
app.include_router(fieldops_router)
app.include_router(fieldops_views_router)