# mms/FieldOps/services/batch_service.py
# FieldOps 项目 - 批次服务层（已完成）

from sqlalchemy.orm import Session
from .batch_model import get_batch_detail, distribute_batch


def get_batch_detail(session: Session, batch_id: str):
    """获取批次详情，包含事件历史和分配的栏位"""
    return get_batch_detail(session, batch_id)


def distribute_batch(session: Session, batch_id: str, distribution_map: dict):
    """执行分栏逻辑，支持多舍多栏分配"""
    return distribute_batch(session, batch_id, distribution_map)