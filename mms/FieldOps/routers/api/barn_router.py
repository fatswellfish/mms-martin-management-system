from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mms.fieldops.database import get_db
from mms.fieldops.models.barn import Barn
from mms.fieldops.schemas.barn_schema import BarnInDB

router = APIRouter(
    prefix="/api/barns",
    tags=["barns"]
)

@router.get("/")
async def read_barns(db: Session = Depends(get_db)):
    barns = db.query(Barn).all()
    return [barn.to_dict() for barn in barns]

@router.get("/{barn_id}")
async def read_barn(barn_id: int, db: Session = Depends(get_db)):
    barn = db.query(Barn).filter(Barn.id == barn_id).first()
    if not barn:
        raise HTTPException(status_code=404, detail="Barn not found")
    return barn.to_dict()
