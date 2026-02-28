from pathlib import Path

# ============================================================
#  classifier.py — 通用分类器
#  基于：目录词 + 业务关键词 + AST tokens（混合策略）
#  输出：类所属的目标模块（字符串）
# ============================================================


class Classifier:
    def __init__(self):
        # 领域关键字映射，可扩展
        # 你可以根据业务调整这些词
        self.domain_keywords = {
            "event_engine": [
                "event", "trace", "trigger", "workflow", "timeline_event",
            ],
            "timeline": [
                "timeline", "period", "batch", "phase",
            ],
            "records": [
                "record", "entry", "log", "history", "measurement", "data",
            ],
            "species": [
                "animal", "species", "pig", "cow", "breed",
            ],
        }

        # 目录关键字 → 域
        # 优先级高于关键字匹配
        self.directory_map = {
            "event_engine": "event_engine",
            "timeline": "timeline",
            "records": "records",
            "species": "species",
        }

    # --------------------------------------------------------
    # 主入口：给定一个 class 的 tokens / path → 返回 domain
    # --------------------------------------------------------
    def classify(self, file_path: Path, class_info):
        """
        file_path: Path
        class_info: ClassInfo（来自 analyzer）
        """

        # 1. 目录词匹配（最高优先级）
        domain = self._directory_classifier(file_path)
        if domain:
            return domain

        # 2. 基于 class 名称 + docstring + methods + tokens 的关键词匹配
        domain = self._keyword_classifier(class_info)
        if domain:
            return domain

        # 3. 无法识别时：返回 None（由 splitter 决定处理）
        return None

    # --------------------------------------------------------
    # 目录规则：modules/**/<dir>/...
    # --------------------------------------------------------
    def _directory_classifier(self, file_path: Path):
        parts = [p.lower() for p in file_path.parts]

        for key, domain_name in self.directory_map.items():
            if key.lower() in parts:
                return domain_name

        return None

    # --------------------------------------------------------
    # 关键字匹配策略（混合）
    # --------------------------------------------------------
    def _keyword_classifier(self, class_info):
        # 合并 tokens
        keywords = class_info.keywords + class_info.methods

        # 把 docstring 也加入 tokens
        if class_info.doc:
            keywords += class_info.doc.lower().replace("_", " ").split()

        keywords = [k.lower() for k in keywords]

        # 遍历领域关键词
        for domain, kw_list in self.domain_keywords.items():
            for kw in kw_list:
                if kw in keywords:
                    return domain

        return None


# ============================================================
# 批量分类入口
# ============================================================

def classify_all(analyses, root: Path):
    c = Classifier()
    results = {}

    for file_analysis in analyses:
        file_path = file_analysis.path
        results[str(file_path)] = []

        for cls in file_analysis.classes:
            domain = c.classify(file_path, cls)
            results[str(file_path)].append((cls.name, domain))

    return results
