import os
from agent.project_context import project_context

ROOT = project_context.project_root

def build_move_patch(move_plan):
    """
    根据 move_plan 生成 git rename patch。
    move_plan: [ { "old": "C:/.../app/xx.py", "new": "modules/.../xx.py" }, ... ]
    """
    diff = ""

    for item in move_plan:
        old_path = item["old"]
        new_path = item["new"]

        old_rel = os.path.relpath(old_path, ROOT).replace("\\", "/")
        new_rel = os.path.relpath(new_path, ROOT).replace("\\", "/")

        diff += f"diff --git a/{old_rel} b/{new_rel}\n"
        diff += "similarity index 100%\n"
        diff += f"rename from {old_rel}\n"
        diff += f"rename to {new_rel}\n\n"

    return diff
