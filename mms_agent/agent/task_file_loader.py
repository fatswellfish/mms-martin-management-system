# task_file_loader.py
# 从 markdown 文件中加载任务，格式为：任务：xxxx

import os

def load_tasks_from_file(path: str):
    if not os.path.exists(path):
        print(f"[task-file] 文件不存在：{path}")
        return []

    tasks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("任务："):
                tasks.append(line.replace("任务：", "", 1).strip())
    return tasks
