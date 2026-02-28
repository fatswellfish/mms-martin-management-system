写入文件 debug_fieldops_routes.py；
内容为：
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from mms.FieldOps.main import app
from fastapi.routing import APIRoute

print("=== FieldOps Routes ===")
for r in app.routes:
    if isinstance(r, APIRoute):
        print(f"{list(r.methods)}  {r.path}")
