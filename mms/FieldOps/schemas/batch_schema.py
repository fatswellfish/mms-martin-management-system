from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BatchBase(BaseModel):
    batch_code: str
    initial_quantity: int
    parent_batch_id: Optional[int] = None
    source_batch_id: Optional[int] = None
    status: str = "active"


class BatchCreate(BatchBase):
    pass


class BatchUpdate(BaseModel):
    initial_quantity: Optional[int] = None
    current_alive: Optional[int] = None
    total_dead: Optional[int] = None
    total_sold_final: Optional[int] = None
    status: Optional[str] = None


class BatchInDB(BatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
