from pathlib import Path

# ============================================================
#  config.py — 通用领域配置（可编辑）
#  用于自动分类、自动拆分、自动重构
# ============================================================

# 项目根路径（可由 dev_agent 注入）
PROJECT_ROOT: Path | None = None


# ------------------------------------------------------------
# 领域关键字映射（你可以随时修改）
# ------------------------------------------------------------
DOMAIN_KEYWORDS = {
    "event_engine": [
        "event", "trace", "trigger", "workflow", "step", "timeline_event",
        "processor", "state", "transition", "engine",
    ],
    "timeline": [
        "timeline", "period", "batch", "phase", "cycle", "window",
        "history", "progress", "milestone",
    ],
    "records": [
        "record", "entry", "log", "history", "measurement", "data",
        "report", "sample", "tracking",
    ],
    "species": [
        "animal", "species", "pig", "cow", "breed", "group", "population",
        "org", "biology", "genetic",
    ],
}


# ------------------------------------------------------------
# 目录映射（优先级最高）
# ------------------------------------------------------------
DIRECTORY_MAP = {
    "event_engine": "event_engine",
    "timeline": "timeline",
    "records": "records",
    "species": "species",
}


# ------------------------------------------------------------
# 默认拆分层（若未来扩展使用）
# ------------------------------------------------------------
DEFAULT_LAYERS = [
    "router", "service", "models", "schemas", "repository"
]
