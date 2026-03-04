from pydantic import BaseModel
from typing import List, Optional

# 位置模型的响应数据结构（用于 API）
class PenResponse(BaseModel):
    id: int
    name: str
    capacity: int
    reserved: bool

class BarnResponse(BaseModel):
    id: int
    name: str
    type: str
    pens: List[PenResponse]

class FarmResponse(BaseModel):
    id: int
    name: str
    barns: List[BarnResponse]