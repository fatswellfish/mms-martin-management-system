import ast
from pathlib import Path

# ============================================================
#  splitter.py — 通用拆分类
#  输入：analyzer + classifier 的结果（类 → domain）
#  输出：拆分计划（不执行写文件）
# ============================================================


class SplitPlanItem:
    """
    拆分类输出结构：
    - class_name: 类名
    - domain: 目标模块（例如 timeline / species）
    - source_file: 原始 .py 文件路径
    - code: 此类的完整源码（字符串）
    """

    def __init__(self, class_name, domain, source_file, code):
        self.class_name = class_name
        self.domain = domain
        self.source_file = source_file
        self.code = code


class Splitter:
    def __init__(self):
        pass

    # --------------------------------------------------------
    # 主入口：基于分析结果生成拆分计划
    # --------------------------------------------------------
    def generate_split_plan(self, analyses, class_map):
        """
        analyses: 来自 analyzer.analyze_directory()
        class_map: { file: [(class_name, domain), ...] } from classifier
        """

        plan = []

        for fa in analyses:
            file_path = str(fa.path)

            if file_path not in class_map:
                continue

            # 读取原始文本，一次性用于切割类定义
            try:
                text = fa.raw_text
                tree = ast.parse(text)
            except Exception:
                continue

            # 收集所有类的 AST 节点
            class_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

            for (class_name, domain) in class_map[file_path]:
                if domain is None:
                    # 不确定的类：跳过或归入 "unsorted"
                    continue

                # 找到对应 class 的 AST
                node = next((n for n in class_nodes if n.name == class_name), None)
                if not node:
                    continue

                # 提取类的完整源码
                class_code = self._extract_class_source(node, text)

                plan.append(
                    SplitPlanItem(
                        class_name=class_name,
                        domain=domain,
                        source_file=file_path,
                        code=class_code,
                    )
                )

        return plan

    # --------------------------------------------------------
    # 提取类源码（从原始文本中按 AST 位置信息切割）
    # --------------------------------------------------------
    def _extract_class_source(self, class_node, raw_text: str):
        """
        基于 AST 的 lineno → col_offset 获取类源码片段
        """
        lines = raw_text.splitlines(True)

        start = class_node.lineno - 1
        end = getattr(class_node, "end_lineno", class_node.lineno)

        # 提取类的完整块（包含方法等）
        block = "".join(lines[start:end])

        return block


# ============================================================
# 工具函数：组合分析 + 分类 → 拆分计划
# ============================================================

def build_split_plan(analyses, class_map):
    splitter = Splitter()
    return splitter.generate_split_plan(analyses, class_map)
