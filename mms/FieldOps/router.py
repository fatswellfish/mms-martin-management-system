from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/fieldops")
templates = Jinja2Templates(directory="mms/fieldops")

@router.get("/", response_class=HTMLResponse)
async def fieldops_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

