from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

# Base model class (assumed to be defined in models/__init__.py)
from .base import Base

class Experiment(Base):
    __tablename__ = 'experiments'

    experiment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="active")  # active, paused, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to scenarios
    scenarios = relationship("Scenario", back_populates="experiment", cascade="all, delete-orphan")

class Scenario(Base):
    __tablename__ = 'scenarios'

    scenario_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id = Column(UUID(as_uuid=True), ForeignKey('experiments.experiment_id'), nullable=False)
    name = Column(String(255), nullable=False)
    parameters = Column(JSON, nullable=False)  # e.g., {"dose": 2, "schedule": ["D0", "D7"]}
    priority = Column(Integer, nullable=False, default=1)  # 1-10

    # Relationship to experiment
    experiment = relationship("Experiment", back_populates="scenarios")

    def to_dict(self):
        return {
            "scenario_id": str(self.scenario_id),
            "experiment_id": str(self.experiment_id),
            "name": self.name,
            "parameters": self.parameters,
            "priority": self.priority
        }

def create_sample_data():
    """Create sample experiment and scenarios for testing."""
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    
    # Create engine (use existing DB URL or fallback to SQLite)
    engine = create_engine("sqlite:///fieldops.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create experiment
    experiment = Experiment(
        name="Vaccine Strategy Comparison",
        status="active"
    )
    session.add(experiment)
    session.flush()  # Get experiment_id
    
    # Create scenarios
    scenarios = [
        Scenario(
            experiment_id=experiment.experiment_id,
            name="A: Standard Dose",
            parameters={"dose": 2, "schedule": ["D0", "D7"]},
            priority=5
        ),
        Scenario(
            experiment_id=experiment.experiment_id,
            name="B: High Dose",
            parameters={"dose": 3, "schedule": ["D0", "D7", "D14"]},
            priority=8
        ),
        Scenario(
            experiment_id=experiment.experiment_id,
            name="C: Phased Approach",
            parameters={"dose": 1.5, "schedule": ["D0", "D14", "D28"]},
            priority=6
        )
    ]
    
    for s in scenarios:
        session.add(s)
    
    session.commit()
    print(f"Created experiment {experiment.experiment_id} with {len(scenarios)} scenarios")
    
    session.close()

if __name__ == "__main__":
    create_sample_data()