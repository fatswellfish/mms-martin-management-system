from sqlalchemy.orm import Session
from mms.FieldOps.models.batch import Batch
from mms.FieldOps.schemas.batch_schema import BatchCreate, BatchUpdate, BatchInDB
from typing import List


def get_batch(db: Session, batch_id: int) -> Batch:
    return db.query(Batch).filter(Batch.id == batch_id).first()

def get_batch_by_code(db: Session, batch_code: str) -> Batch:
    return db.query(Batch).filter(Batch.batch_code == batch_code).first()

def get_batches(db: Session, skip: int = 0, limit: int = 100) -> List[Batch]:
    return db.query(Batch).offset(skip).limit(limit).all()

def create_batch(db: Session, batch: BatchCreate) -> Batch:
    db_batch = Batch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

def update_batch(db: Session, batch_id: int, batch_update: BatchUpdate) -> Batch:
    db_batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not db_batch:
        return None
    for key, value in batch_update.dict(exclude_unset=True).items():
        setattr(db_batch, key, value)
    db_batch.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_batch)
    return db_batch

def delete_batch(db: Session, batch_id: int) -> bool:
    db_batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not db_batch:
        return False
    db.delete(db_batch)
    db.commit()
    return True
