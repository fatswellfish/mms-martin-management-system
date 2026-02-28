from fastapi import FastAPI
from .router import router as farm_router

app = FastAPI(title="Farm System")
app.include_router(farm_router)
