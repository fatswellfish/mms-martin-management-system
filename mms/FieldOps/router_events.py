from fastapi import APIRouter
from mms.FieldOps.services.events_service import list_events

router = APIRouter(prefix="/FieldOps/api", tags=["FieldOps Events"])

@router.get("/events")
def api_events(limit: int = 50):
    return list_events(limit=limit)

