from fastapi import APIRouter
from mms.fieldops.services.events_service import list_events

router = APIRouter(prefix="/fieldops/api", tags=["fieldops Events"])

@router.get("/events")
def api_events(limit: int = 50):
    return list_events(limit=limit)

