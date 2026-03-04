from pydantic import BaseModel
from typing import Optional


class BarnBase(BaseModel):
    name: str
    category_id: int
    description: Optional[str] = None


class BarnCreate(BarnBase):
    pass


class BarnUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None


class BarnInDB(BarnBase):
    id: int

    class Config:
        from_attributes = True
