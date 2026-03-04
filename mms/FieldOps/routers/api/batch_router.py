from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from mms.FieldOps.database import get_db
from mms.FieldOps.models.batch import Batch
from mms.FieldOps.schemas.batch_schema import BatchCreate, BatchUpdate, BatchInDB
from mms.FieldOps.services.batch_service import (
    get_batch,
    get_batch_by_code,
    get_batches,
    create_batch,
    update_batch,
    delete_batch
)

router = APIRouter(
    prefix="/api/batches",
    tags=["batches"]
)

@router.get("/")
async def read_batches(skip: int = Query(0), limit: int = Query(100), db: Session = Depends(get_db)):
    batches = get_batches(db, skip=skip, limit=limit)
    return [batch.to_dict() for batch in batches]

@router.get("/{batch_id}")
async def read_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = get_batch(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch.to_dict()

@router.get("/code/{batch_code}")
async def read_batch_by_code(batch_code: str, db: Session = Depends(get_db)):
    batch = get_batch_by_code(db, batch_code)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found by code")
    return batch.to_dict()

@router.post("/")
async def create_new_batch(batch: BatchCreate, db: Session = Depends(get_db)):
    db_batch = create_batch(db, batch)
    return db_batch.to_dict()

@router.put("/{batch_id}")
async def update_existing_batch(batch_id: int, batch_update: BatchUpdate, db: Session = Depends(get_db)):
    updated_batch = update_batch(db, batch_id, batch_update)
    if not updated_batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return updated_batch.to_dict()

@router.delete("/{batch_id}")
async def delete_batch_item(batch_id: int, db: Session = Depends(get_db)):
    success = delete_batch(db, batch_id)
    if not success:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"message": "Batch deleted successfully"}
