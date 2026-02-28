from pathlib import Path
from .splitter import SplitPlanItem

class FileWriter:
    def __init__(self, project_root: Path):
        self.root = project_root

    def write(self, split_plan: list[SplitPlanItem]):
        results = []

        for item in split_plan:
            domain = item.domain
            class_name = item.class_name
            code = item.code

            # ---- 正确路径：写入 mms/modules/... 下
            module_dir = self.root / "mms" / "modules" / "domain_operations" / "farm_domain" / domain
            module_dir.mkdir(parents=True, exist_ok=True)

            out_path = module_dir / f"{class_name}.py"

            out_path.write_text(code, encoding="utf-8")

            results.append({
                "class": class_name,
                "domain": domain,
                "output": str(out_path)
            })

        return results

def write_split_results(root: Path, split_plan):
    writer = FileWriter(root)
    return writer.write(split_plan)
