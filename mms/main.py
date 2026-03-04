from fastapi import FastAPI
from mms.FieldOps.routers import main_router
from mms.FieldOps.database import init_db

# 创建 FastAPI 应用实例
def create_app():
    app = FastAPI(title="FieldOps - 现场运维系统", description="基于 ISO9001 框架的养殖场管理平台")
    
    # 包含所有路由（包括 API）
    app.include_router(main_router.create_main_router())
    
    # 初始化数据库表结构（首次运行时）
    init_db()
    
    return app

# 生成应用实例
class FieldOpsApp:
    def __init__(self):
        self.app = create_app()
    
    def get_app(self):
        return self.app

# 实例化并导出应用（供 Uvicorn 启动）
app = FieldOpsApp().get_app()