import os
from agent.project_context import project_context

def scan_project_tree():
    root = project_context.project_root
    print("[scan] 扫描中…")
    output = []
    for r, dirs, files in os.walk(root):
        if ".git" in r or ".venv" in r:
            continue
        rel = os.path.relpath(r, root)
        if rel == ".":
            rel = "(project root)"
        output.append(rel + "/")
        for f in files:
            output.append("    " + os.path.relpath(os.path.join(r, f), root))
    print("[scan] 完成。")
    return "\n".join(output)
