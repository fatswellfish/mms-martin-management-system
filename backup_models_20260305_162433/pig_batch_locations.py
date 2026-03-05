from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UUID, event
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
from datetime import datetime
import uuid

class PigBatchLocation(Base):
    __tablename__ = 'pig_batch_locations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = Column(UUID(as_uuid=True), ForeignKey('batches.id'), nullable=False)
    location_type = Column(String(50), nullable=False)  # "farm", "barn", "pen", "transfer"
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(String(20))
    longitude = Column(String(20))
    notes = Column(String(500))
    metadata = Column(JSONB, nullable=True)
    
    # Relationships
    batch = relationship("Batch", backref="locations")
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "batch_id": str(self.batch_id),
            "location_type": self.location_type,
            "timestamp": self.timestamp.isoformat(),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "notes": self.notes,
            "metadata": self.metadata or {}
        }
    
    def __repr__(self):
        return f"<PigBatchLocation(id={self.id}, batch_id={self.batch_id}, type={self.location_type})>"

# Optional: Add event listener for automatic timestamp on insert
@event.listens_for(PigBatchLocation, "before_insert")
def set_timestamp(mapper, connection, target):
    if not target.timestamp:
        target.timestamp = datetime.utcnow()