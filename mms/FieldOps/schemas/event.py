from pydantic import BaseModel
from datetime import datetime

class EventSchema(BaseModel):
    id: int
    event_type: str
    level: str
    farm_id: int | None
    barn_id: int | None
    pen_id: int | None
    batch_id: int | None
    quantity: int | None
    actor: str | None
    timestamp: datetime
    message: str
    severity: str
    color: str

    class Config:
        orm_mode = True