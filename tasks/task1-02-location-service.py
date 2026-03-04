# mms/FieldOps/services/location_service.py

from sqlalchemy.orm import Session
from .models.location import Farm, Barn, Pen
from typing import List, Dict, Optional

def get_farm_tree(db: Session) -> Dict:
    """
    获取完整的农场结构树，包含所有层级：
    - 农场 (Farm)
    - 猪舍 (Barn) → 按类型分组（产房、保育、育肥等）
    - 猪栏 (Pen) → 显示当前数量与预留状态
    """
    try:
        farms = db.query(Farm).all()
        result = []
        
        for farm in farms:
            barns_by_type = {}
            
            # 按猪舍类型分组
            for barn in farm.barns:
                barn_type = barn.barn_type
                if barn_type not in barns_by_type:
                    barns_by_type[barn_type] = []
                
                # 构建猪栏列表（含当前数量和预留状态）
                pens = [
                    {
                        "id": pen.id,
                        "name": pen.name,
                        "capacity": pen.capacity,
                        "current_quantity": pen.current_quantity,
                        "is_reserved": pen.is_reserved
                    }
                    for pen in barn.pens
                ]
                
                barn_data = {
                    "id": barn.id,
                    "name": barn.name,
                    "barn_type": barn.barn_type,
                    "capacity": barn.capacity,
                    "is_reserved": barn.is_reserved,
                    "pens": pens
                }
                barns_by_type[barn_type].append(barn_data)
            
            farm_data = {
                "id": farm.id,
                "name": farm.name,
                "barns_by_type": barns_by_type
            }
            result.append(farm_data)
            
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_barn_pens(db: Session, barn_id: int) -> Dict:
    """
    获取指定猪舍的所有栏位信息，用于前端卡片展示。
    """
    try:
        barn = db.query(Barn).filter(Barn.id == barn_id).first()
        
        if not barn:
            return {
                "success": False,
                "error": "Barn not found"
            }
        
        pens = [
            {
                "id": pen.id,
                "name": pen.name,
                "capacity": pen.capacity,
                "current_quantity": pen.current_quantity,
                "is_reserved": pen.is_reserved
            }
            for pen in barn.pens
        ]
        
        return {
            "success": True,
            "data": {
                "barn_id": barn.id,
                "barn_name": barn.name,
                "barn_type": barn.barn_type,
                "pens": pens
            }
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def distribute_batch(db: Session, batch_id: str, distribution_map: Dict[str, int]) -> Dict:
    """
    执行批次分栏逻辑：将一批猪分配到多个猪舍和栏位。
    distribution_map: {"barn_id_1": 30, "barn_id_2": 20} → 分配 30 头到第1舍，20 头到第2舍
    """
    try:
        # 这里仅做模拟实现，实际需结合 Batch 表逻辑（待后续实现）
        total_assigned = sum(distribution_map.values())
        
        # 验证总数量是否合理（示例：600头）
        if total_assigned != 600:
            return {
                "success": False,
                "error": f"Total assigned ({total_assigned}) does not match expected batch size (600)"
            }
        
        # 模拟更新栏位数量（实际应通过 ORM 操作）
        # 此处仅返回成功响应，不修改数据库（等待后续实现）
        
        return {
            "success": True,
            "message": f"Batch {batch_id} distributed successfully to {len(distribution_map)} barns",
            "details": distribution_map
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }