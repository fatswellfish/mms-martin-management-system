from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from mms.FieldOps.database import get_db
from mms.FieldOps.models.event import Event
from mms.FieldOps.schemas.event_schema import EventCreate, EventUpdate, EventInDB
from mms.FieldOps.services.event_service import (
    get_event,
    get_events,
    create_event,
    update_event,
    delete_event
)

router = APIRouter(
    prefix="/api/events",
    tags=["events"]
)

@router.get("/")
async def read_events(skip: int = Query(0), limit: int = Query(50), db: Session = Depends(get_db)):
    events = get_events(db, skip=skip, limit=limit)
    return [event.to_dict() for event in events]

@router.get("/{event_id}")
async def read_event(event_id: int, db: Session = Depends(get_db)):
    event = get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.to_dict()

@router.post("/")
async def create_new_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = create_event(db, event)
    return db_event.to_dict()

@router.put("/{event_id}")
async def update_existing_event(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db)):
    updated_event = update_event(db, event_id, event_update)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event.to_dict()

@router.delete("/{event_id}")
async def delete_event_item(event_id: int, db: Session = Depends(get_db)):
    success = delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}
