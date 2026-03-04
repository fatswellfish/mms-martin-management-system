from sqlalchemy.orm import Session
from mms.FieldOps.models.event import Event
from mms.FieldOps.schemas.event_schema import EventCreate, EventUpdate, EventInDB
from typing import List
from datetime import datetime


def get_event(db: Session, event_id: int) -> Event:
    return db.query(Event).filter(Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 50) -> List[Event]:
    return db.query(Event).order_by(Event.timestamp.desc()).offset(skip).limit(limit).all()

def create_event(db: Session, event: EventCreate) -> Event:
    # 自动设置颜色（基于事件类型）
    from mms.FieldOps.models.event import get_event_color
    color = get_event_color(event.event_type)
    
    db_event = Event(
        event_type=event.event_type,
        level=event.level,
        farm_id=event.farm_id,
        barn_id=event.barn_id,
        pen_id=event.pen_id,
        batch_id=event.batch_id,
        quantity=event.quantity,
        actor=event.actor,
        message=event.message,
        severity=event.severity,
        color=color
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: EventUpdate) -> Event:
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None
    for key, value in event_update.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    # 重新计算颜色（如果事件类型被修改）
    if "event_type" in event_update.dict(exclude_unset=True):
        from mms.FieldOps.models.event import get_event_color
        db_event.color = get_event_color(event_update.event_type)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return False
    db.delete(db_event)
    db.commit()
    return True
