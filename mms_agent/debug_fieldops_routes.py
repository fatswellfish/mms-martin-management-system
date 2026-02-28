import sys
from pathlib import Path

# 关键修复：把 “project 根目录” 加入 sys.path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from mms.FieldOps.main import app
from fastapi.routing import APIRoute

print("=== FieldOps Routes ===")
for r in app.routes:
    if isinstance(r, APIRoute):
        print(f"{list(r.methods)}  {r.path}")