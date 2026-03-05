from fastapi import APIRouter
from typing import List
from mms.fieldops.models.location import Farm, Barn, Pen
from mms.fieldops.schemas.location import FarmResponse, BarnResponse, PenResponse

# 位置相关路由
def create_location_router() -> APIRouter:
    router = APIRouter()
    
    @router.get("/tree", response_model=List[FarmResponse])
    def get_farm_tree():
        # 模拟数据：获取所有农场及其结构（实际应从数据库查询）
        farms = [
            Farm(
                id=1,
                name="绿源养殖场",
                barns=[
                    Barn(
                        id=101,
                        name="育肥舍",
                        type="fattening",
                        pens=[
                            Pen(id=1001, name="A区", capacity=50, reserved=False),
                            Pen(id=1002, name="B区", capacity=50, reserved=False)
                        ]
                    ),
                    Barn(
                        id=102,
                        name="产房",
                        type="parturition",
                        pens=[
                            Pen(id=1003, name="C区", capacity=10, reserved=True)
                        ]
                    )
                ]
            )
        ]
        
        return farms
    
    @router.get("/barn/{barn_id}/pens", response_model=List[PenResponse])
    def get_barn_pens(barn_id: int):
        # 模拟根据 barn_id 获取猪栏信息（实际应从数据库查询）
        if barn_id == 101:
            return [
                Pen(id=1001, name="A区", capacity=50, reserved=False),
                Pen(id=1002, name="B区", capacity=50, reserved=False)
            ]
        elif barn_id == 102:
            return [
                Pen(id=1003, name="C区", capacity=10, reserved=True)
            ]
        else:
            raise HTTPException(status_code=404, detail="Barn not found")
    
    return router