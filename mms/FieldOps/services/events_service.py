from sqlalchemy.orm import Session
from app.db.orm_engine import SessionLocal
from mms.fieldops.models.event import Event, get_event_color


def list_events(limit: int = 50):
    db: Session = SessionLocal()
    rows = db.query(Event).order_by(Event.timestamp.desc()).limit(limit).all()
    db.close()

    result = []
    for e in rows:
        result.append({
            "id": e.id,
            "event_type": e.event_type,
            "level": e.level,
            "farm_id": e.farm_id,
            "barn_id": e.barn_id,
            "pen_id": e.pen_id,
            "batch_id": e.batch_id,
            "quantity": e.quantity,
            "actor": e.actor,
            "timestamp": e.timestamp.isoformat(),
            "message": e.message,
            "severity": e.severity,
            "color": e.color or get_event_color(e.event_type)
        })
    return result

