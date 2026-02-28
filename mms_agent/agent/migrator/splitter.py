import os
import re
from agent.project_context import project_context

ROOT = project_context.project_root


class Splitter:

    def __init__(self):
        pass

    # -----------------------------
    # 基础：解析文件内容
    # -----------------------------
    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # -----------------------------
    # 解析路由函数（FastAPI）
    # -----------------------------
    def extract_routes(self, text):
        """
        提取所有 @router.get/post/... 路由函数
        返回： [ "def xxx(...)", ... ]
        """
        routes = []
        pattern = r"@router\.(get|post|put|delete|patch)[\s\S]*?def\s+\w+\([^\)]*\):[\s\S]*?(?=\n@router|\Z)"
        for match in re.finditer(pattern, text):
            routes.append(match.group(0))
        return routes

    # -----------------------------
    # 提取 Pydantic schemas
    # -----------------------------
    def extract_schemas(self, text):
        pattern = r"class\s+\w+\(BaseModel\):[\s\S]*?(?=\nclass|\Z)"
        schemas = re.findall(pattern, text)
        return schemas

    # -----------------------------
    # 提取 ORM models
    # -----------------------------
    def extract_models(self, text):
        pattern = r"class\s+\w+\(Base\):[\s\S]*?(?=\nclass|\Z)"
        models = re.findall(pattern, text)
        return models

    # -----------------------------
    # 提取 service 方法（非路由、非模型、非 schema）
    # -----------------------------
    def extract_services(self, text):
        routes = self.extract_routes(text)
        schemas = self.extract_schemas(text)
        models = self.extract_models(text)

        consumed = "\n\n".join(routes + schemas + models)
        remaining = text

        # 移除路由 / schema / model 的代码段
        for block in routes + schemas + models:
            remaining = remaining.replace(block, "")

        # 剩下的 def 就是 service 层候选
        pattern = r"def\s+\w+\([^\)]*\):[\s\S]*?(?=\ndef|\Z)"
        services = re.findall(pattern, remaining)

        # 过滤掉空和注释
        cleaned = []
        for s in services:
            if "pass" in s or s.strip().startswith("#"):
                continue
            cleaned.append(s)

        return cleaned

    # -----------------------------
    # 拆分文件为多模块
    # -----------------------------
    def split_file(self, old_path, target_root):
        text = self.load(old_path)

        routes = self.extract_routes(text)
        schemas = self.extract_schemas(text)
        models = self.extract_models(text)
        services = self.extract_services(text)

        result = {}

        # router
        if routes:
            router_path = os.path.join(target_root, "router.py")
            result[router_path] = "\n\n".join(routes)

        # service
        if services:
            service_path = os.path.join(target_root, "service.py")
            result[service_path] = "\n\n".join(services)

        # repository（暂为空，下一阶段生成）
        repo_path = os.path.join(target_root, "repository.py")
        if repo_path not in result:
            result[repo_path] = "``  # TODO: repository generated later"

        # models
        if models:
            models_path = os.path.join(target_root, "models.py")
            result[models_path] = "\n\n".join(models)

        # schemas
        if schemas:
            schemas_path = os.path.join(target_root, "schemas.py")
            result[schemas_path] = "\n\n".join(schemas)

        return result


splitter = Splitter()
