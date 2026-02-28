import ast
from pathlib import Path

# ============================================================
#   analyzer.py  —  通用 AST 分析器
#   输出结构化的代码信息，用于分类与拆分
# ============================================================


class ClassInfo:
    def __init__(self, name, methods, doc, decorators, keywords):
        self.name = name
        self.methods = methods        # list[str]
        self.doc = doc                # class docstring
        self.decorators = decorators  # class decorators
        self.keywords = keywords      # tokens from names/docstring


class FileAnalysis:
    def __init__(self, path):
        self.path = path
        self.imports = []
        self.classes = []             # list[ClassInfo]
        self.functions = []           # standalone functions
        self.raw_text = ""
        self.tokens = []              # keywords extracted from identifiers / comments / strings


class Analyzer:
    """
    通用 AST 分析器：
    - 解析 imports
    - 解析类、方法
    - 解析装饰器
    - 抽取领域关键字（基于 identifiers / docstring / literal strings）
    """

    def __init__(self):
        pass

    # --------------------------
    # 主入口：分析文件
    # --------------------------
    def analyze_file(self, path: Path) -> FileAnalysis:
        result = FileAnalysis(path)

        try:
            text = path.read_text(encoding="utf-8")
            result.raw_text = text
            tree = ast.parse(text)
        except Exception:
            return result

        self._extract_imports(tree, result)
        self._extract_classes(tree, result)
        self._extract_functions(tree, result)
        self._extract_tokens(result)

        return result

    # --------------------------
    # import 收集
    # --------------------------
    def _extract_imports(self, tree, result: FileAnalysis):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    result.imports.append(name.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                result.imports.append(module)

    # --------------------------
    # 类/方法/装饰器/注释
    # --------------------------
    def _extract_classes(self, tree, result: FileAnalysis):
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                name = node.name
                methods = []
                decorators = []
                docstring = ast.get_docstring(node)

                for dec in node.decorator_list:
                    try:
                        decorators.append(self._decorator_to_str(dec))
                    except:
                        pass

                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef):
                        methods.append(sub.name)

                keywords = self._keyword_extract(name, docstring, methods)

                info = ClassInfo(
                    name=name,
                    methods=methods,
                    doc=docstring,
                    decorators=decorators,
                    keywords=keywords,
                )
                result.classes.append(info)

    # --------------------------
    # 普通函数
    # --------------------------
    def _extract_functions(self, tree, result: FileAnalysis):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                result.functions.append(node.name)

    # --------------------------
    # decorator 转字符串
    # --------------------------
    def _decorator_to_str(self, dec):
        if isinstance(dec, ast.Attribute):
            return dec.attr
        if isinstance(dec, ast.Name):
            return dec.id
        if isinstance(dec, ast.Call):
            if isinstance(dec.func, ast.Name):
                return dec.func.id
            if isinstance(dec.func, ast.Attribute):
                return dec.func.attr
        return str(dec)

    # --------------------------
    # 抽取关键字
    # --------------------------
    def _keyword_extract(self, name, docstring, methods):
        k = set()

        def push(words):
            if not words:
                return
            for w in words.lower().replace("_", " ").split():
                if w.isalpha():
                    k.add(w)

        push(name)
        if docstring:
            push(docstring)

        for m in methods:
            push(m)

        return list(k)

    # --------------------------
    # 从原始文件扫描 token（注释/字符串）
    # --------------------------
    def _extract_tokens(self, result: FileAnalysis):
        text = result.raw_text.lower()

        # 简单 token 提取
        words = []
        for token in text.replace("_", " ").split():
            if token.isalpha():
                words.append(token)

        result.tokens = list(set(words))


# ============================================================
# 工具函数：批量分析目录
# ============================================================

def analyze_directory(root: Path):
    analyzer = Analyzer()
    results = []

    for py in root.rglob("*.py"):
        if "__pycache__" in str(py):
            continue
        results.append(analyzer.analyze_file(py))

    return results
