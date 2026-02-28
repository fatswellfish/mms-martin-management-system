import sys
from pathlib import Path
import ast

BASE = Path(__file__).resolve().parents[3]
SRC = BASE / "mms_legacy/modules/domain_operations/farm_domain"
DST_ROUTER = BASE / "mms/farm_app/router.py"
DST_SERVICE_DIR = BASE / "mms/farm_app/service"

def extract_api_functions(path: Path):
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for deco in node.decorator_list:
                if isinstance(deco, ast.Call) and hasattr(deco.func, "attr"):
                    if deco.func.attr in ["get", "post", "put", "delete"]:
                        funcs.append(node)
    return funcs

def run():
    print("=== FARM API AUTO MIGRATE ===")
    DST_ROUTER.write_text("from fastapi import APIRouter\nrouter = APIRouter(prefix=\"/farm\", tags=[\"farm\"])\n\n", encoding="utf-8")

    DST_SERVICE_DIR.mkdir(parents=True, exist_ok=True)

    for py in SRC.glob("*.py"):
        funcs = extract_api_functions(py)
        if not funcs:
            continue

        print(f"发现 API 于 {py.name}：{len(funcs)} 个")

        # 写入 router
        with DST_ROUTER.open("a", encoding="utf-8") as f:
            for func in funcs:
                f.write(f"@router.get('/{func.name}')\n")
                f.write(f"async def {func.name}():\n")
                f.write(f"    return {{\"message\": \"{func.name} migrated\"}}\n\n")

    print("=== DONE ===")

if __name__ == '__main__':
    run()