from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mms.fieldops.database import get_db
from mms.fieldops.models.category import Category
from mms.fieldops.models.barn import Barn
from mms.fieldops.models.pen import Pen
from mms.fieldops.schemas.tree_schema import TreeResponse

router = APIRouter(
    prefix="/api/tree",
    tags=["tree"]
)

@router.get("/")
async def get_tree_structure(db: Session = Depends(get_db)):
    # 1. 获取所有类别（分类）
    categories = db.query(Category).all()
    
    # 2. 为每个类别获取其下的猪舍（Barn）
    tree_data = []
    for category in categories:
        barns = db.query(Barn).filter(Barn.category_id == category.id).all()
        
        # 3. 为每个猪舍获取其下的栏位（Pen）
        barn_list = []
        for barn in barns:
            pens = db.query(Pen).filter(Pen.barn_id == barn.id).all()
            
            # 将栏位数据转换为字典，包含当前批次信息（如果存在）
            pen_list = []
            for pen in pens:
                current_batch = None
                if pen.current_batch_id:
                    batch = db.query(Batch).filter(Batch.id == pen.current_batch_id).first()
                    if batch:
                        current_batch = {
                            "batch_code": batch.batch_code,
                            "quantity": pen.current_quantity or 0
                        }
                
                pen_list.append({
                    "id": pen.id,
                    "name": pen.name,
                    "capacity": pen.capacity,
                    "is_reserved": bool(pen.is_reserved),
                    "current_batch": current_batch
                })
            
            barn_list.append({
                "id": barn.id,
                "name": barn.name,
                "barn_type": category.name,
                "pens": pen_list
            })
        
        tree_data.append({
            "id": category.id,
            "name": category.name,
            "barns": barn_list
        })
    
    return TreeResponse(tree=tree_data)
