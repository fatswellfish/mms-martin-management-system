写入文件 mms/FieldOps/router_views.py；
内容为：
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

# 基础 loader：加载 FieldOps 根目录
templates = Jinja2Templates(directory="mms/FieldOps")

# ======= 关键修复：自动重写 farm/* 到 FieldOps 的真实目录 =======
# Jinja 模板会先把 template 名字传给 loader，我们在 loader 前做路径替换。
def rewrite_template_name(name: str) -> str:
    if name.startswith("farm/"):
        return "views/farm_domain/" + name.split("/",1)[1]
    return name

# monkeypatch TemplateResponse 来重写模板路径
_original_template_response = templates.TemplateResponse
def _patched_template_response(name, context, *args, **kwargs):
    new_name = rewrite_template_name(name)
    return _original_template_response(new_name, context, *args, **kwargs)

templates.TemplateResponse = _patched_template_response
# ================================================================

router = APIRouter(prefix="/FieldOps", tags=["FieldOps Views"])

def view(template: str):
    async def _view(request: Request):
        return templates.TemplateResponse(template, {"request": request})
    return _view

# farm_domain pages
router.get("/farm-home", response_class=HTMLResponse)(view("views/farm_domain/farm_home.html"))
router.get("/farm-tree", response_class=HTMLResponse)(view("views/farm_domain/pig_farm_tree.html"))
router.get("/farm-structure", response_class=HTMLResponse)(view("views/farm_domain/pig_farm_structure.html"))

# field_ops/pages
router.get("/barn-view", response_class=HTMLResponse)(view("views/field_ops/pages/barn_view.html"))
router.get("/batch-detail", response_class=HTMLResponse)(view("views/field_ops/pages/batch_detail.html"))
router.get("/category-view", response_class=HTMLResponse)(view("views/field_ops/pages/category_view.html"))
router.get("/dashboard", response_class=HTMLResponse)(view("views/field_ops/pages/dashboard.html"))
router.get("/dashboard-tree", response_class=HTMLResponse)(view("views/field_ops/pages/dashboard_tree.html"))
router.get("/event-trace", response_class=HTMLResponse)(view("views/field_ops/pages/event_trace.html"))
router.get("/inbound-wizard", response_class=HTMLResponse)(view("views/field_ops/pages/inbound_wizard.html"))
router.get("/mass-event-wizard", response_class=HTMLResponse)(view("views/field_ops/pages/mass_event_wizard.html"))
router.get("/pen-detail", response_class=HTMLResponse)(view("views/field_ops/pages/pen_detail.html"))
