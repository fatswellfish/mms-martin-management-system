from pydantic import BaseModel
from typing import List, Optional

# 批次模型的响应数据结构（用于 API）
class BatchResponse(BaseModel):
    id: int
    batch_id: str
    quantity: int
    status: str