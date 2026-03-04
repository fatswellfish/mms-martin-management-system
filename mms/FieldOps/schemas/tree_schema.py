from pydantic import BaseModel
from typing import List, Optional


class PenNode(BaseModel):
    id: int
    name: str
    capacity: int
    is_reserved: bool
    current_batch: Optional[dict] = None  # {"batch_code": "20260228", "quantity": 15}


class BarnNode(BaseModel):
    id: int
    name: str
    barn_type: str  # 产房、保育、育肥等
    pens: List[PenNode]


class CategoryNode(BaseModel):
    id: int
    name: str
    barns: List[BarnNode]


class TreeResponse(BaseModel):
    tree: List[CategoryNode]
