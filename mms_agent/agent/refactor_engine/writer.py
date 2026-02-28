from pathlib import Path
from .splitter import SplitPlanItem

# ============================================================
#  writer.py — 通用文件写入器（落盘 + 导入修复）
# ============================================================


class FileWriter:
    def __init__(self, project_root: Path):
        self.root = project_root

        # 标准 DDD 分层目录
        self.default_layers = ["router", "service", "models", "schemas", "repository"]

    # --------------------------------------------------------
    # 写入拆分类项目（按 domain 分类）
    # --------------------------------------------------------
    def write(self, split_plan: list[SplitPlanItem]):
        """
        split_plan: List[SplitPlanItem]
        """
        results = []

        for item in split_plan:
            domain = item.domain  # e.g. timeline / species
            class_name = item.class_name
            source = item.source_file
            code = item.code

            # 生成文件输出位置
            module_dir = self.root / "modules" / "domain_operations" / "farm_domain" / domain

            # 不存在则创建（通用）
            module_dir.mkdir(parents=True, exist_ok=True)

            # 文件名：class 名字作为文件名
            out_path = module_dir / f"{class_name}.py"

            # 修复 import（目前基于简单规则，后续可增强）
            fixed_code = self._fix_imports(code, domain)

            # 写入最终文件
            out_path.write_text(fixed_code, encoding="utf-8")

            results.append({
                "class": class_name,
                "domain": domain,
                "source": source,
                "output": str(out_path),
            })

        return results

    # --------------------------------------------------------
    # 简单 import 修复逻辑（使用相对路径规则）
    # --------------------------------------------------------
    def _fix_imports(self, code: str, domain: str) -> str:
        """
        当前版本：简单 import 修复（可后续增强）
        - 替换旧 farm_domain.* 路径为 farm_domain.<domain>.*
        """

        code_lines = code.splitlines()
        fixed = []

        for line in code_lines:
            if "farm_domain" in line:
                # 将 import farm_domain.xxxx 替换为 domain 文件夹
                line = line.replace("farm_domain.", f"farm_domain.{domain}.")
            fixed.append(line)

        return "\n".join(fixed)


# ============================================================
# 入口：执行写操作
# ============================================================

def write_split_results(root: Path, split_plan):
    writer = FileWriter(root)
    return writer.write(split_plan)
