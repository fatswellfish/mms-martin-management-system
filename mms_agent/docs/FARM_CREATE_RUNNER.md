写入文件 mms/run_farm.py；
内容为：
from fastapi import FastAPI
from mms.mms_agent_farm_loader import load_farm_modules

app = FastAPI(title="FARM Standalone System")

load_farm_modules(app)


写入文件 mms/mms_agent_farm_loader.py；
内容为：
import importlib
import pkgutil
from fastapi import FastAPI

BASE_PACKAGE = "mms.modules.domain_operations.farm_domain"

def load_farm_modules(app: FastAPI):
    try:
        pkg = importlib.import_module(BASE_PACKAGE)
    except Exception as e:
        print("无法加载 FARM 根目录:", e)
        return

    print("[farm_loader] scanning farm submodules...")

    for _, module_name, ispkg in pkgutil.walk_packages(pkg.__path__, BASE_PACKAGE + "."):
        if not ispkg:
            continue

        print("[farm_loader] loading:", module_name)

        try:
            router_mod = importlib.import_module(module_name + ".router")
            if hasattr(router_mod, "router"):
                app.include_router(router_mod.router)
                print("  -> router mounted")
        except Exception:
            pass

    print("[farm_loader] done.")
