创建目录 mms/farm_app/；
创建目录 mms/farm_app/service/；
创建目录 mms/farm_app/schemas/；
创建目录 mms/farm_app/models/；
创建目录 mms/farm_app/repository/；

写入文件 mms/farm_app/main.py；
内容为：
from fastapi import FastAPI
from .router import router as farm_router

app = FastAPI(title="Farm System")
app.include_router(farm_router)

写入文件 mms/farm_app/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/farm", tags=["farm"])
