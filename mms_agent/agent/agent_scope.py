from pathlib import Path

# ==========================================
# 权限系统（最终稳定版本）
# ==========================================

# ★ 使用运行时工作目录作为项目根目录 ★
PROJECT_ROOT = Path.cwd()

ALLOWED_ROOTS = [
    str(PROJECT_ROOT / "mms"),
    str(PROJECT_ROOT / "mms_test"),
    str(PROJECT_ROOT / "mms_agent"),
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
    print("\n========== DEBUG ==========")
    print("INPUT PATH:", path)
    print("NORMALIZED:", normalize(path))
    print("ALLOWED ROOTS:")
    for a in ALLOWED_ROOTS:
        print("  ", normalize(a))
    print("===========================\n")

    if is_denied(path):
        raise PermissionError(f"[DENY] 禁止访问路径: {path}")
    if is_read_only(path):
        raise PermissionError(f"[READ_ONLY] 禁止写入路径: {path}")
    if not is_allowed(path):
        raise PermissionError(f"[OUT_OF_SCOPE] 不在允许范围: {path}")
    return True

def validate_read(path: str):
    if is_denied(path):
        raise PermissionError(f"[DENY] 禁止访问路径: {path}")
    return True
