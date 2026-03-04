# mms/FieldOps/services/location_service.py
# FieldOps 项目 - 位置服务层（已完成）

from sqlalchemy.orm import Session
from .location_model import get_farm_tree, get_barn_pens


def get_farm_tree(session: Session):
    """获取完整的农场结构树，用于前端渲染"""
    return get_farm_tree(session)


def get_barn_pens(session: Session, barn_id: int):
    """获取某猪舍的所有栏位及占用情况"""
    return get_barn_pens(session, barn_id)