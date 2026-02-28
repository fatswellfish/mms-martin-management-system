写入文件 mms/FieldOps/base.html；
内容为：
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>{% block title %}FieldOps{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/style.css">

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
