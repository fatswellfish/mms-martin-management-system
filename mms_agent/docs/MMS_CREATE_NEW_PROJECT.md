# 创建全新 MMS 插件化项目骨架

创建目录 mms/；
创建目录 mms/runtime/；
创建目录 mms/runtime/db/；
创建目录 mms/modules/；
创建目录 mms/templates/；
创建目录 mms/templates/components/；
创建目录 mms/static/；
创建目录 mms/static/css/；
创建目录 mms/static/js/；
创建目录 mms/tools/；

写入文件 mms/runtime/main.py；
内容为：
from fastapi import FastAPI
from .module_loader import load_modules

app = FastAPI(title="MMS System")
load_modules(app)

写入文件 mms/runtime/module_loader.py；
内容为：
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

写入文件 mms/runtime/module_registry.py；
内容为：
MODULES = {}
def register_module(name: str, meta: dict):
    MODULES[name] = meta

写入文件 mms/runtime/settings.py；
内容为：
TEMPLATE_PATHS = []
STATIC_PATHS = []

写入文件 mms/runtime/db/orm.py；
内容为：
# ORM placeholder

写入文件 mms/runtime/db/init_db.py；
内容为：
# DB init placeholder

写入文件 mms/templates/base.html；
内容为：
<!DOCTYPE html>
<html>
<head>
    <title>{{ title or "MMS" }}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    {% include "components/nav.html" %}
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>

写入文件 mms/templates/components/nav.html；
内容为：
<nav><h3>MMS Navigation</h3></nav>

写入文件 mms/static/css/style.css；
内容为：
/* global css */

写入文件 mms/static/js/app.js；
内容为：
console.log("MMS loaded");


# system_core
创建目录 mms/modules/system_core/；
创建目录 mms/modules/system_core/templates/；
创建目录 mms/modules/system_core/static/；

写入文件 mms/modules/system_core/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/system-core", tags=["system_core"])

写入文件 mms/modules/system_core/service.py；
内容为：
class SystemCoreService: pass

写入文件 mms/modules/system_core/models.py；
内容为：
class SystemCoreModel: pass

写入文件 mms/modules/system_core/schemas.py；
内容为：
class SystemCoreSchema: pass

写入文件 mms/modules/system_core/repository.py；
内容为：
class SystemCoreRepository: pass


# domain_operations/farm_domain
创建目录 mms/modules/domain_operations/；
创建目录 mms/modules/domain_operations/farm_domain/；

# event_engine
创建目录 mms/modules/domain_operations/farm_domain/event_engine/；
创建目录 mms/modules/domain_operations/farm_domain/event_engine/templates/；
创建目录 mms/modules/domain_operations/farm_domain/event_engine/static/；

写入文件 mms/modules/domain_operations/farm_domain/event_engine/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/farm/event-engine", tags=["farm_event_engine"])

写入文件 mms/modules/domain_operations/farm_domain/event_engine/service.py；
内容为：
class EventEngineService: pass

写入文件 mms/modules/domain_operations/farm_domain/event_engine/models.py；
内容为：
class EventEngineModel: pass

写入文件 mms/modules/domain_operations/farm_domain/event_engine/schemas.py；
内容为：
class EventEngineSchema: pass

写入文件 mms/modules/domain_operations/farm_domain/event_engine/repository.py；
内容为：
class EventEngineRepository: pass


# timeline
创建目录 mms/modules/domain_operations/farm_domain/timeline/；
创建目录 mms/modules/domain_operations/farm_domain/timeline/templates/；
创建目录 mms/modules/domain_operations/farm_domain/timeline/static/；

写入文件 mms/modules/domain_operations/farm_domain/timeline/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/farm/timeline", tags=["farm_timeline"])

写入文件 mms/modules/domain_operations/farm_domain/timeline/models.py；
内容为：
class FarmTimelineModel: pass

写入文件 mms/modules/domain_operations/farm_domain/timeline/schemas.py；
内容为：
class FarmTimelineSchema: pass

写入文件 mms/modules/domain_operations/farm_domain/timeline/repository.py；
内容为：
class FarmTimelineRepository: pass

写入文件 mms/modules/domain_operations/farm_domain/timeline/service.py；
内容为：
class FarmTimelineService: pass


# species
创建目录 mms/modules/domain_operations/farm_domain/species/；
创建目录 mms/modules/domain_operations/farm_domain/species/templates/；
创建目录 mms/modules/domain_operations/farm_domain/species/static/；

写入文件 mms/modules/domain_operations/farm_domain/species/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/farm/species", tags=["farm_species"])

写入文件 mms/modules/domain_operations/farm_domain/species/models.py；
内容为：
class FarmSpeciesModel: pass

写入文件 mms/modules/domain_operations/farm_domain/species/schemas.py；
内容为：
class FarmSpeciesSchema: pass

写入文件 mms/modules/domain_operations/farm_domain/species/repository.py；
内容为：
class FarmSpeciesRepository: pass

写入文件 mms/modules/domain_operations/farm_domain/species/service.py；
内容为：
class FarmSpeciesService: pass


# records
创建目录 mms/modules/domain_operations/farm_domain/records/；
创建目录 mms/modules/domain_operations/farm_domain/records/templates/；
创建目录 mms/modules/domain_operations/farm_domain/records/static/；

写入文件 mms/modules/domain_operations/farm_domain/records/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/farm/records", tags=["farm_records"])

写入文件 mms/modules/domain_operations/farm_domain/records/models.py；
内容为：
class FarmRecordsModel: pass

写入文件 mms/modules/domain_operations/farm_domain/records/schemas.py；
内容为：
class FarmRecordsSchema: pass

写入文件 mms/modules/domain_operations/farm_domain/records/repository.py；
内容为：
class FarmRecordsRepository: pass

写入文件 mms/modules/domain_operations/farm_domain/records/service.py；
内容为：
class FarmRecordsService: pass


# Q1
创建目录 mms/modules/Q1_organization_and_planning/；
创建目录 mms/modules/Q1_organization_and_planning/templates/；
创建目录 mms/modules/Q1_organization_and_planning/static/；

写入文件 mms/modules/Q1_organization_and_planning/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/q1", tags=["q1"])

# Q2
创建目录 mms/modules/Q2_support_processes/；
创建目录 mms/modules/Q2_support_processes/templates/；
创建目录 mms/modules/Q2_support_processes/static/；

写入文件 mms/modules/Q2_support_processes/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/q2", tags=["q2"])

# Q3
创建目录 mms/modules/Q3_operational_processes/；
创建目录 mms/modules/Q3_operational_processes/templates/；
创建目录 mms/modules/Q3_operational_processes/static/；

写入文件 mms/modules/Q3_operational_processes/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/q3", tags=["q3"])

# Q4
创建目录 mms/modules/Q4_performance_and_improvement/；
创建目录 mms/modules/Q4_performance_and_improvement/templates/；
创建目录 mms/modules/Q4_performance_and_improvement/static/；

写入文件 mms/modules/Q4_performance_and_improvement/router.py；
内容为：
from fastapi import APIRouter
router = APIRouter(prefix="/q4", tags=["q4"])
