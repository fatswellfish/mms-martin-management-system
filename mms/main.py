# mms/main.py
from fastapi import FastAPI
from .fieldops.routers.main_router import create_main_router

# 1. 创建应用实例
app = FastAPI(title="FieldOps", description="Farm Management System")

# 2. 导入所有模型，确保类注册到 SQLAlchemy Base
import mms.fieldops.models  # ✅ 强制导入所有模型，触发注册

# 3. 包含主路由（/fieldops）
app.include_router(create_main_router(), prefix="/fieldops")

# 4. 启动时打印信息
def startup_event():
    print("✅ FieldOps 系统已启动，路由 /fieldops 已加载.")

app.add_event_handler("startup", startup_event)

# 5. 暴露 API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)