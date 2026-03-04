from sqlalchemy.orm import Session
from ..models.batch import Batch
from ..models.pig_batch_locations import PigBatchLocation
from ..schemas.pig_batch_location_schema import PigBatchLocationCreate
from ..schemas.batch_schema import BatchInDB
from typing import List

def create_batch(db: Session, batch_data):
    db_batch = Batch(
        batch_code=batch_data.batch_code,
        initial_quantity=batch_data.initial_quantity,
        current_alive=batch_data.initial_quantity,
        total_dead=0,
        total_sold_final=0,
        status="active"
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

def get_batch(db: Session, batch_id):
    return db.query(Batch).filter(Batch.id == batch_id).first()

def get_batches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Batch).offset(skip).limit(limit).all()

def update_batch(db: Session, batch_id: str, batch_data):
    db_batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not db_batch:
        return None
    for key, value in batch_data.dict(exclude_unset=True).items():
        setattr(db_batch, key, value)
    db.commit()
    db.refresh(db_batch)
    return db_batch

def delete_batch(db: Session, batch_id: str):
    db_batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not db_batch:
        return False
    db.delete(db_batch)
    db.commit()
    return True

def add_location_to_batch(db: Session, batch_id: str, location_data: PigBatchLocationCreate) -> PigBatchLocationSchema:
    """Add a new location record to a batch."""
    # First, ensure the batch exists
    db_batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not db_batch:
        raise ValueError(f"Batch with id {batch_id} not found")
    
    # Create the location entry
    location = PigBatchLocation(
        batch_id=batch_id,
        location_type=location_data.location_type,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
        notes=location_data.notes,
        metadata=location_data.metadata or {}
    )
    
    db.add(location)
    db.commit()
    db.refresh(location)
    
    # Return the created location as a schema object
    return PigBatchLocationSchema(
        id=location.id,
        batch_id=location.batch_id,
        location_type=location.location_type,
        timestamp=location.timestamp,
        latitude=location.latitude,
        longitude=location.longitude,
        notes=location.notes,
        metadata=location.metadata
    )