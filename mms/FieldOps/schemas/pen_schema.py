from pydantic import BaseModel
from typing import Optional


class PenBase(BaseModel):
    name: str
    barn_id: int
    capacity: int = 0
    is_reserved: bool = False
    description: Optional[str] = None


class PenCreate(PenBase):
    pass


class PenUpdate(BaseModel):
    name: Optional[str] = None
    barn_id: Optional[int] = None
    capacity: Optional[int] = None
    is_reserved: Optional[bool] = None
    description: Optional[str] = None


class PenInDB(PenBase):
    id: int

    class Config:
        from_attributes = True
