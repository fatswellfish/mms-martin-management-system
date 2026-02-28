写入文件 debug_fieldops_routes.py；
内容为：
from mms.FieldOps.main import app
from fastapi.routing import APIRoute

print("=== FieldOps Routes ===")
for r in app.routes:
    if isinstance(r, APIRoute):
        print(f"{list(r.methods)}  {r.path}")
