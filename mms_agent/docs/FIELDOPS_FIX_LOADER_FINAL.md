写入文件 mms/FieldOps/router_views.py；
内容为：
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, ChoiceLoader

# -------------------------------
# 真实搜索路径（一次性保证存在）
# -------------------------------
loader = ChoiceLoader([
    FileSystemLoader("mms/FieldOps"),
    FileSystemLoader("mms/FieldOps/views"),
    FileSystemLoader("mms/FieldOps/views/farm_domain"),
    FileSystemLoader("mms/FieldOps/views/field_ops/pages"),
])

env = Environment(loader=loader)

templates = Jinja2Templates(directory="mms/FieldOps")
templates.env = env


# -------------------------------
# 重写 farm/ 前缀 → farm_domain/
# -------------------------------
def rewrite_name(name: str) -> str:
    if name.startswith("farm/"):
        return "views/farm_domain/" + name.split("/", 1)[1]
    return name

_original = templates.TemplateResponse

def patched(name, context, *args, **kwargs):
    return _original(rewrite_name(name), context, *args, **kwargs)

templates.TemplateResponse = patched


# -------------------------------
# Routers
# -------------------------------
router = APIRouter(prefix="/FieldOps", tags=["FieldOps Views"])

def view(template: str):
    async def _view(request: Request):
        return templates.TemplateResponse(template, {"request": request})
    return _view


router.get("/farm-home", response_class=HTMLResponse)(view("views/farm_domain/farm_home.html"))
router.get("/farm-tree", response_class=HTMLResponse)(view("views/farm_domain/pig_farm_tree.html"))
router.get("/farm-structure", response_class=HTMLResponse)(view("views/farm_domain/pig_farm_structure.html"))

router.get("/barn-view", response_class=HTMLResponse)(view("views/field_ops/pages/barn_view.html"))
router.get("/batch-detail", response_class=HTMLResponse)(view("views/field_ops/pages/batch_detail.html"))
router.get("/category-view", response_class=HTMLResponse)(view("views/field_ops/pages/category_view.html"))
router.get("/dashboard", response_class=HTMLResponse)(view("views/field_ops/pages/dashboard.html"))
router.get("/dashboard-tree", response_class=HTMLResponse)(view("views/field_ops/pages/dashboard_tree.html"))
router.get("/event-trace", response_class=HTMLResponse)(view("views/field_ops/pages/event_trace.html"))
router.get("/inbound-wizard", response_class=HTMLResponse)(view("views/field_ops/pages/inbound_wizard.html"))
router.get("/mass-event-wizard", response_class=HTMLResponse)(view("views/field_ops/pages/mass_event_wizard.html"))
router.get("/pen-detail", response_class=HTMLResponse)(view("views/field_ops/pages/pen_detail.html"))
