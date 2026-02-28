# 自动迁移 FARM Domain（模式 A）

执行 FARM 全自动迁移；
来源目录：mms_legacy/modules/domain_operations/farm_domain；

写入文件 mms_agent/agent/migrator/farm_auto_migrate.py；
内容为：
import os
from pathlib import Path
from mms_agent.agent.refactor_engine.analyzer import analyze_directory
from mms_agent.agent.refactor_engine.classifier import classify_all
from mms_agent.agent.refactor_engine.splitter import build_split_plan
from mms_agent.agent.refactor_engine.writer import write_split_results

BASE = Path.cwd()
SRC = BASE / "mms_legacy/modules/domain_operations/farm_domain"
DST = BASE / "mms/modules/domain_operations/farm_domain"

def run():
    analyses = analyze_directory(SRC)
    class_map = classify_all(analyses, SRC)
    plan = build_split_plan(analyses, class_map)
    write_split_results(BASE, plan)

if __name__ == "__main__":
    run()

