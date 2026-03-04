# mms/FieldOps/models/base.py
# FieldOps 项目 - ORM 基础模型（已完成）

from sqlalchemy.ext.declarative import declarative_base

# 1. 创建基础模型类（所有模型继承自 Base）
Base = declarative_base()

# 2. 可选：添加通用方法（如 to_dict）到基类中（此处不实现，保持简洁）
# 3. 项目已通过 `models/location.py`、`models/batch.py` 等文件使用该基类