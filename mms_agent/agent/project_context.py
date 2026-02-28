import os

class ProjectContext:
    """
    提供项目范围信息、结构边界信息、路径信息、模块域信息。
    dev_agent 和所有子模块都必须通过该类获取环境信息。
    """

    def __init__(self):
        # 自动识别项目根目录
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # 项目名称（文件夹名）
        self.project_name = os.path.basename(self.project_root)

        # 固定目录（系统边界），agent 只能在这些目录内操作
        self.modules_dir = os.path.join(self.project_root, "modules")
        self.docs_dir = os.path.join(self.project_root, "docs")
        self.app_dir = os.path.join(self.project_root, "app")

        # 未来旧系统位置（迁移 FARM 用）
        self.legacy_dirs = [
            os.path.join(self.project_root, "app"),
            os.path.join(self.project_root, "templates"),
            os.path.join(self.project_root, "static"),
            os.path.join(self.project_root, "sql"),
            os.path.join(self.project_root, "sqlite"),
            os.path.join(self.project_root, "uploads"),
        ]

        # agent 能修改的范围（白名单）
        self.write_whitelist = [
            self.modules_dir,           # 新模块
            self.docs_dir,              # 文档
            os.path.join(self.project_root, "agent"),   # agent 子模块
        ]

        # agent 不得修改的范围（黑名单）
        self.write_blacklist = [
            os.path.join(self.project_root, ".venv"),
            os.path.join(self.project_root, ".git"),
        ]

    def in_workspace(self, path):
        """检查 agent 是否允许写入该路径"""
        path = os.path.abspath(path)
        for denied in self.write_blacklist:
            if path.startswith(os.path.abspath(denied)):
                return False
        for allowed in self.write_whitelist:
            if path.startswith(os.path.abspath(allowed)):
                return True
        return False

# 单例（所有模块引用它）
project_context = ProjectContext()
