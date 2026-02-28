import os
from agent.project_context import project_context

PROJECT_PATH = project_context.project_root

def find_target_file(task):
    """现在仅匹配 modules/ 下文件，未来可扩展到 legacy"""
    modules_root = os.path.join(PROJECT_PATH, "modules")
    for root, dirs, files in os.walk(modules_root):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), PROJECT_PATH).replace("\\", "/")
            if rel in task:
                return rel
            if f in task:
                return rel
    return None
