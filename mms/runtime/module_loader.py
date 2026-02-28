import importlib
import pkgutil
from fastapi import FastAPI

BASE_PACKAGE = "project.mms.modules"

def load_modules(app: FastAPI):
    print("[module_loader] scanning modules...")
    try:
        base = importlib.import_module(BASE_PACKAGE)
    except Exception as e:
        print("无法加载模块根目录:", e)
        return

    for _, name, ispkg in pkgutil.walk_packages(base.__path__, BASE_PACKAGE + "."):
        if not ispkg:
            continue
        print("[module_loader] loading:", name)
        try:
            pkg = importlib.import_module(name)
        except Exception:
            continue

        try:
            router = importlib.import_module(name + ".router")
            if hasattr(router, "router"):
                app.include_router(router.router)
        except Exception:
            pass

    print("[module_loader] all modules loaded.")
