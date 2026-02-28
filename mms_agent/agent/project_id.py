import os

def get_project_root():
    """
    返回当前项目的根目录路径。
    自动根据本文件位置推断，不依赖硬编码路径。
    """
    # 本文件在：<project_root>/agent/project_id.py
    # 向上一层目录就是项目根目录
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_project_name():
    """
    返回项目名称（文件夹名）。
    """
    return os.path.basename(get_project_root())

def describe_project():
    """
    返回项目的基础识别信息，方便 agent 在任务中使用。
    """
    root = get_project_root()
    name = get_project_name()
    return {
        "project_name": name,
        "project_root": root,
        "modules_dir": os.path.join(root, "modules"),
        "docs_dir": os.path.join(root, "docs"),
        "app_dir": os.path.join(root, "app")
    }
