写入文件 mms_agent/agent/agent_scope.py；
内容为：
from pathlib import Path

# 项目根目录允许写入
PROJECT_ROOT = Path.cwd()

ALLOWED_ROOTS = [
    str(PROJECT_ROOT),
    str(PROJECT_ROOT / "mms"),
    str(PROJECT_ROOT / "mms_agent"),
    str(PROJECT_ROOT / "mms_test"),
]

READ_ONLY = [
    str(PROJECT_ROOT / "mms_legacy"),
]

DENY = [
    "C:/Windows",
    "C:/Program Files",
]

def normalize(path: str) -> str:
    return str(Path(path).as_posix()).lower()

def is_denied(path: str) -> bool:
    p = normalize(path)
    return any(p.startswith(normalize(d)) for d in DENY)

def is_read_only(path: str) -> bool:
    p = normalize(path)
    return any(p.startswith(normalize(ro)) for ro in READ_ONLY)

def is_allowed(path: str) -> bool:
    p = normalize(path)
    return any(p.startswith(normalize(a)) for a in ALLOWED_ROOTS)

def validate_write(path: str):
    if is_denied(path):
        raise PermissionError(f"[DENY] {path}")
    if is_read_only(path):
        raise PermissionError(f"[READ_ONLY] {path}")
    if not is_allowed(path):
        raise PermissionError(f"[OUT_OF_SCOPE] {path}")
    return True

def validate_read(path: str):
    if is_denied(path):
        raise PermissionError(f"[DENY] {path}")
    return True
