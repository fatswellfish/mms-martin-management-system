写入文件 debug_scan_includes.py；
内容为：
from pathlib import Path
import re

root = Path("mms/FieldOps/views")
pattern = re.compile(r'\{% *include *"([^"]+)" *%}')

print("=== Scanning all includes ===")
for html in root.rglob("*.html"):
    lines = html.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line in lines:
        m = pattern.search(line)
        if m:
            print(f"{html}  →  include: '{m.group(1)}'")
