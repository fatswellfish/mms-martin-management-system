from fastapi import FastAPI
from mms.fieldops.main import app as fieldops_app

# 导出应用实例，供主系统导入
__all__ = ["fieldops_app"]
