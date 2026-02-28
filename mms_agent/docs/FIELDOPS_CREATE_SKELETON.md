创建目录 mms/FieldOps/；
创建目录 mms/FieldOps/views/；
创建目录 mms/FieldOps/static/；
创建目录 mms/FieldOps/schemas/；
创建目录 mms/FieldOps/services/；
创建目录 mms/FieldOps/models/；

写入文件 mms/FieldOps/base.html；
内容为：
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>{% block title %}FieldOps{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
    <style>
        .topbar {background:#2c3e50;color:white;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;font-size:15px;}
        .topbar-title {font-size:18px;font-weight:bold;color:#ecf0f1;}
        .topbar-nav a {color:#ecf0f1;text-decoration:none;margin:0 10px;padding:4px 6px;border-radius:4px;display:inline-block;font-size:14px;}
        .topbar-nav a:hover {background-color:#34495e;}
        .page-container {padding:20px;}
    </style>
</head>
<body>
    <div class="topbar">
        <div class="topbar-title">FieldOps</div>
        <div class="topbar-nav">
            <a href="/FieldOps">首页</a>
            <a href="/FieldOps/tree">农场结构</a>
            <a href="/FieldOps/batch">批次管理</a>
            <a href="/FieldOps/event">事件轨迹</a>
            <a href="/FieldOps/wizard">向导</a>
        </div>
    </div>
    <div class="page-container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>


写入文件 mms/FieldOps/index.html；
内容为：
{% extends "FieldOps/base.html" %}
{% block title %}FieldOps Dashboard{% endblock %}
{% block content %}
<h2>FieldOps · 现场运维 Dashboard</h2>
<p class="text-muted" style="font-size:13px;">猪场结构、批次、事件、栏位、向导入口。</p>
<hr>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;">
    <div class="qms-block"><h4>Farm Tree</h4><a href="/FieldOps/tree">进入 ▸</a></div>
    <div class="qms-block"><h4>Batch Overview</h4><a href="/FieldOps/batch">进入 ▸</a></div>
    <div class="qms-block"><h4>Event Trace</h4><a href="/FieldOps/event">进入 ▸</a></div>
    <div class="qms-block"><h4>Barn / Pen View</h4><a href="/FieldOps/barn">进入 ▸</a></div>
    <div class="qms-block"><h4>Inbound Wizard</h4><a href="/FieldOps/wizard/inbound">进入 ▸</a></div>
    <div class="qms-block"><h4>Mass Event Wizard</h4><a href="/FieldOps/wizard/mass">进入 ▸</a></div>
</div>
{% endblock %}


写入文件 mms/FieldOps/router.py；
内容为：
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/FieldOps")
templates = Jinja2Templates(directory="mms/FieldOps")

@router.get("/", response_class=HTMLResponse)
async def fieldops_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


写入文件 mms/FieldOps/main.py；
内容为：
from fastapi import FastAPI
from .router import router as fieldops_router

app = FastAPI(title="FieldOps")
app.include_router(fieldops_router)
