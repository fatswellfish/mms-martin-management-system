import os
import ast
import re
from pathlib import Path

# ============================================================
#   MMS — System Topology Analyzer
#   扫描 Python / HTML / JS 并生成系统拓扑数据
# ============================================================

API_PATTERN = re.compile(r'["\'](/[^"\']+)["\']')
FETCH_PATTERN = re.compile(r'fetch\(["\'](/[^"\']+)["\']')
AXIOS_PATTERN = re.compile(r'axios\.(get|post)\(["\'](/[^"\']+)["\']')
HX_PATTERN = re.compile(r'hx-(get|post)=["\'](/[^"\']+)["\']')

# ------------------------------------------------------------
# 扫描所有文件
# ------------------------------------------------------------
def collect_files(root: Path):
    py_files = []
    html_files = []
    js_files = []

    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if p.suffix == ".py":
            py_files.append(p)
        elif p.suffix in [".html", ".htm"]:
            html_files.append(p)
        elif p.suffix in [".js"]:
            js_files.append(p)

    return py_files, html_files, js_files


# ------------------------------------------------------------
# 解析 Python import
# ------------------------------------------------------------
def parse_python_imports(py_file: Path):
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
    except:
        return []

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            imports.append(mod)

    return imports


# ------------------------------------------------------------
# 扫描 HTML 模板中的 API 路径
# ------------------------------------------------------------
def extract_html_api(html_file: Path):
    text = html_file.read_text(encoding="utf-8", errors="ignore")
    found = set()

    for pattern in [API_PATTERN, FETCH_PATTERN, AXIOS_PATTERN, HX_PATTERN]:
        for m in pattern.findall(text):
            if isinstance(m, tuple):
                found.add(m[-1])
            else:
                found.add(m)
    return list(found)


# ------------------------------------------------------------
# 扫描 JS 文件中的 API
# ------------------------------------------------------------
def extract_js_api(js_file: Path):
    text = js_file.read_text(encoding="utf-8", errors="ignore")
    found = set()

    for pattern in [API_PATTERN, FETCH_PATTERN, AXIOS_PATTERN]:
        for m in pattern.findall(text):
            if isinstance(m, tuple):
                found.add(m[-1])
            else:
                found.add(m)
    return list(found)


# ------------------------------------------------------------
# 模块归类
# ------------------------------------------------------------
def classify_module(path: Path, root: Path):
    rel = str(path.relative_to(root))

    if rel.startswith("app/"):
        return "app"

    if rel.startswith("modules/system_core"):
        return "system_core"

    if rel.startswith("modules/domain_operations/farm_domain"):
        return "farm_domain"

    if rel.startswith("modules/"):
        return "domain_operations"

    if rel.startswith("templates/"):
        return "templates"

    if rel.startswith("static/"):
        return "static"

    return "other"


# ------------------------------------------------------------
# 顶层接口：生成拓扑结构（data dict）
# ------------------------------------------------------------
def build_topology(root: Path):
    py_files, html_files, js_files = collect_files(root)

    topology = {
        "python": [],
        "html": [],
        "js": [],
        "imports": {},
        "html_api": {},
        "js_api": {},
        "module_class": {},
    }

    # Python
    for py in py_files:
        topology["python"].append(str(py))
        topology["imports"][str(py)] = parse_python_imports(py)
        topology["module_class"][str(py)] = classify_module(py, root)

    # HTML
    for h in html_files:
        topology["html"].append(str(h))
        topology["html_api"][str(h)] = extract_html_api(h)
        topology["module_class"][str(h)] = classify_module(h, root)

    # JS
    for j in js_files:
        topology["js"].append(str(j))
        topology["js_api"][str(j)] = extract_js_api(j)
        topology["module_class"][str(j)] = classify_module(j, root)

    return topology


# ------------------------------------------------------------
# 渲染为 markdown
# ------------------------------------------------------------
def topology_to_markdown(topo: dict):
    out = []

    out.append("# SYSTEM TOPOLOGY MAP\n")
    out.append("自动生成\n")

    out.append("\n## Python Files\n")
    for f in topo["python"]:
        out.append(f"- {f}")

    out.append("\n## HTML Templates\n")
    for f in topo["html"]:
        out.append(f"- {f}")

    out.append("\n## JavaScript Files\n")
    for f in topo["js"]:
        out.append(f"- {f}")

    out.append("\n## Imports\n")
    for f, imps in topo["imports"].items():
        out.append(f"\n### {f}")
        for i in imps:
            out.append(f"- {i}")

    out.append("\n## HTML API Routes\n")
    for f, apis in topo["html_api"].items():
        out.append(f"\n### {f}")
        for a in apis:
            out.append(f"- {a}")

    out.append("\n## JS API Routes\n")
    for f, apis in topo["js_api"].items():
        out.append(f"\n### {f}")
        for a in apis:
            out.append(f"- {a}")

    out.append("\n## Module Classification\n")
    for f, c in topo["module_class"].items():
        out.append(f"- {f} → {c}")

    return "\n".join(out)
