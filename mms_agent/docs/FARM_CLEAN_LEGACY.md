写入文件 mms_agent/agent/migrator/farm_clean_legacy.py；
内容为：
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
SRC = BASE / "mms_legacy/modules/domain_operations/farm_domain"

# 会删除含中文、GPT说明、DSL指令、非 Python 有害行
PATTERNS_REMOVE = [
    r"以下是.*", 
    r"完整代码如下.*",
    r"内容为：.*",
    r"写入文件.*",
    r"创建目录.*",
    r"```.*",
    r"：",            # 中文冒号
    r"；",            # 中文分号
    r"。",            # 中文句号
    r"[^\x00-\x7F]+", # 非 ASCII 字符（包括中文）
]

def clean_line(line: str):
    for pat in PATTERNS_REMOVE:
        if re.search(pat, line):
            return ""  # 删除整行
    return line

def clean_file(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    cleaned = []
    for line in lines:
        new_line = clean_line(line)
        if new_line.strip().startswith("#"):
            continue
        cleaned.append(new_line)

    cleaned_text = "\n".join(cleaned)
    path.write_text(cleaned_text, encoding="utf-8")
    print(f"清理完成：{path.name}")

def run():
    print("=== CLEAN FARM LEGACY FILES ===")
    for py in SRC.glob("*.py"):
        clean_file(py)
    print("=== DONE ===")

if __name__ == "__main__":
    run()
