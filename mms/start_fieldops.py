import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 正确导入并运行应用
if __name__ == "__main__":
    from .FieldOps.routers import main_router
    from fastapi import FastAPI
    
    app = FastAPI(title="FieldOps - 现场运维系统", description="基于 ISO9001 框架的养殖场管理平台")
    app.include_router(main_router)
    
    # 启动应用（此处简化为打印提示）
    print("FieldOps 主页服务已启动。访问 http://localhost:8000/ 可查看主页。")
    print("> Press Ctrl+C to stop.")
    
    # 模拟运行（实际应使用 Uvicorn）
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down...")