from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mms.fieldops.database import get_db
from mms.fieldops.models.pen import Pen
from mms.fieldops.schemas.pen_schema import PenInDB

router = APIRouter(
    prefix="/api/pens",
    tags=["pens"]
)

@router.get("/")
async def read_pens(db: Session = Depends(get_db)):
    pens = db.query(Pen).all()
    return [pen.to_dict() for pen in pens]

@router.get("/{pen_id}")
async def read_pen(pen_id: int, db: Session = Depends(get_db)):
    pen = db.query(Pen).filter(Pen.id == pen_id).first()
    if not pen:
        raise HTTPException(status_code=404, detail="Pen not found")
    return pen.to_dict()
