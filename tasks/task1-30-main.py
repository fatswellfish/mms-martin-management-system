# mms/FieldOps/main.py
# FieldOps 项目 - 主程序入口（已完成）

from fastapi import FastAPI
from .router import main_router
from .database import engine, Base
import uvicorn

# 创建应用实例
app = FastAPI(
    title="FieldOps - 现场管理系统",
    description="一个模块化、可扩展的养殖场现场管理平台，支持实时监控与智能调度。",
    version="1.0.0"
)

# 包含所有路由（前缀为 /FieldOps）
app.include_router(main_router, prefix="/FieldOps")

# 启动时创建数据库表结构（仅在开发环境）
@app.on_event("startup")
async def startup_event():
    print("🔄 正在初始化数据库...")
    try:
        # 为简化演示，直接创建所有表（实际部署中应使用 Alembic 迁移）
        Base.metadata.create_all(bind=engine)
        print("✅ 所有数据库表已成功创建")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")

# 根路径返回静态文件（前端入口）
@app.get("/")
async def read_root():
    return {"message": "Welcome to FieldOps! Visit /FieldOps to access the frontend."}

# 用于测试的健康检查接口（供监控系统使用）
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2026-03-04T18:02:00Z"}

# 启动命令：uvicorn main:app --reload
if __name__ == "__main__":
    print("🚀 FieldOps 服务启动中...")
    print("🌐 访问地址: http://localhost:8000")
    print("📊 接口文档: http://localhost:8000/docs")
    print("🔧 健康检查: http://localhost:8000/health")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)