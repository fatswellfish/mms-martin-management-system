import sys
from pathlib import Path

# ---------------------------------------------------------
#  修复 Python 模块路径
# ---------------------------------------------------------
BASE = Path(__file__).resolve().parents[3]   # project 根目录
sys.path.insert(0, str(BASE))

from mms_agent.agent.refactor_engine.analyzer import analyze_directory
from mms_agent.agent.refactor_engine.classifier import classify_all
from mms_agent.agent.refactor_engine.splitter import build_split_plan
from mms_agent.agent.refactor_engine.writer import write_split_results

SRC = BASE / "mms_legacy/modules/domain_operations/farm_domain"
DST = BASE / "mms/modules/domain_operations/farm_domain"


def run():
    print("=== FARM AUTO MIGRATE START ===")
    print("SRC:", SRC)
    print("DST:", DST)

    # 1. 分析所有 legacy FARM 文件
    analyses = analyze_directory(SRC)
    print("分析完成：", len(analyses), "个文件")

    # 2. 分类所有类（event_engine / timeline / species / records）
    class_map = classify_all(analyses, SRC)
    print("分类完成")

    # 3. 构建拆分计划
    plan = build_split_plan(analyses, class_map)
    print("拆分计划生成：", len(plan), "个类")

    # 4. 写入新的 MMS 模块结构
    results = write_split_results(BASE, plan)
    print("写入完成：", len(results), "个文件")

    print("=== FARM AUTO MIGRATE DONE ===")


if __name__ == "__main__":
    run()
