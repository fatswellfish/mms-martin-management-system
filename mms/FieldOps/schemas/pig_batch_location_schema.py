from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class PigBatchLocationBase(BaseModel):
    batch_id: UUID
    location_type: str  # "farm", "barn", "pen", "transfer"
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None


class PigBatchLocationCreate(PigBatchLocationBase):
    pass

class PigBatchLocationUpdate(PigBatchLocationBase):
    pass

class PigBatchLocationSchema(BaseModel):
    id: UUID
    batch_id: UUID
    location_type: str
    timestamp: datetime
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True