import ast
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
SRC = BASE / "mms_legacy/modules/domain_operations/farm_domain"

def clean_file(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")

    # 尝试 AST parse，如失败，则逐行剥离非法代码
    try:
        ast.parse(text)
        print(f"[OK] {path.name} (no change)")
        return
    except:
        print(f"[CLEAN] {path.name}")

    lines = text.splitlines()
    cleaned_lines = []

    buffer = ""
    for line in lines:
        test = buffer + line + "\n"
        try:
            ast.parse(test)
            buffer += line + "\n"
        except:
            # 此行非法，直接跳过
            pass

    cleaned_text = buffer
    path.write_text(cleaned_text, encoding="utf-8")

def run():
    print("=== AST CLEAN START ===")
    for py in SRC.glob("*.py"):
        clean_file(py)
    print("=== AST CLEAN DONE ===")

if __name__ == "__main__":
    run()