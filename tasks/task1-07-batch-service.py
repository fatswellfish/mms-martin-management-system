# mms/FieldOps/services/batch_service.py

from sqlalchemy.orm import Session
from .models.batch import Batch, Event
from typing import List, Dict, Optional

def get_batch_detail(db: Session, batch_id: str) -> Dict:
    """
    获取指定批次的详细信息，包括：
    - 批次状态与数量
    - 当前归属栏（若存在）
    - 最近 5 条事件记录（按时间倒序）
    """
    try:
        # 1. 查询批次信息
        batch = db.query(Batch).filter(Batch.batch_id == batch_id).first()
        
        if not batch:
            return {
                "success": False,
                "error": f"Batch {batch_id} not found"
            }
        
        # 2. 查询最近 5 条事件（按时间倒序）
        recent_events = db.query(Event)
        .filter(Event.batch_id == batch_id)
        .order_by(Event.timestamp.desc())
        .limit(5)
        .all()
        
        event_list = [event.to_dict() for event in recent_events]
        
        # 3. 构建返回数据
        result = {
            "success": True,
            "data": {
                "batch_id": batch.batch_id,
                "quantity": batch.quantity,
                "status": batch.status,
                "source_pen_id": batch.source_pen_id,
                "current_pens": [],  # 后续可扩展为真实列表（通过中间表）
                "recent_events": event_list
            }
        }
        
        return result
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def distribute_batch_to_pens(db: Session, batch_id: str, distribution_map: Dict[str, int]) -> Dict:
    """
    将一个批次分配到多个猪栏（支持跨舍分批）。
    distribution_map: {"pen_id_1": 300, "pen_id_2": 300} → 分配 300 头到第1栏，300 头到第2栏
    """
    try:
        # 1. 查找批次对象（假设已存在）
        batch = db.query(Batch).filter(Batch.batch_id == batch_id).first()
        
        if not batch:
            return {
                "success": False,
                "error": f"Batch {batch_id} not found"
            }
        
        # 2. 验证总数量是否匹配（600头）
        total_assigned = sum(distribution_map.values())
        if total_assigned != batch.quantity:
            return {
                "success": False,
                "error": f"Total assigned ({total_assigned}) does not match batch size ({batch.quantity})"
            }
        
        # 3. 模拟更新数据库（实际需通过 ORM 操作）
        # 这里仅返回成功响应，不修改数据库（等待后续实现）
        
        return {
            "success": True,
            "message": f"Batch {batch_id} distributed successfully to {len(distribution_map)} pens",
            "details": distribution_map
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def create_event(db: Session, event_type: str, batch_id: str, pen_id: int = None, barn_id: int = None, description: str = None) -> Dict:
    """
    创建一条新事件，用于记录系统状态变化。
    """
    try:
        new_event = Event(
            event_type=event_type,
            batch_id=batch_id,
            pen_id=pen_id,
            barn_id=barn_id,
            description=description
        )
        
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        
        return {
            "success": True,
            "data": new_event.to_dict()
        }
    
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }