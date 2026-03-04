from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    event_type: str  # transfer, death, sale, vaccination, illness_mild, illness_severe
    level: str  # FARM, BARN, PEN, BATCH
    farm_id: Optional[int] = None
    barn_id: Optional[int] = None
    pen_id: Optional[int] = None
    batch_id: Optional[int] = None
    quantity: Optional[int] = None
    actor: Optional[str] = None
    message: str
    severity: str  # info, warning, error, critical


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    event_type: Optional[str] = None
    level: Optional[str] = None
    farm_id: Optional[int] = None
    barn_id: Optional[int] = None
    pen_id: Optional[int] = None
    batch_id: Optional[int] = None
    quantity: Optional[int] = None
    actor: Optional[str] = None
    message: Optional[str] = None
    severity: Optional[str] = None


class EventInDB(EventBase):
    id: int
    timestamp: datetime
    color: str

    class Config:
        from_attributes = True
