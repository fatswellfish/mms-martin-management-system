from sqlalchemy.orm import Session
from mms.FieldOps.models.experiment import Experiment
from mms.FieldOps.schemas.experiment_schema import ExperimentCreate, ExperimentUpdate, ExperimentInDB
from typing import List
from datetime import datetime


def get_experiment(db: Session, experiment_id: int) -> Experiment:
    return db.query(Experiment).filter(Experiment.id == experiment_id).first()

def get_experiments(db: Session, skip: int = 0, limit: int = 100) -> List[Experiment]:
    return db.query(Experiment).offset(skip).limit(limit).all()

def create_experiment(db: Session, experiment: ExperimentCreate) -> Experiment:
    db_experiment = Experiment(**experiment.dict())
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment

def update_experiment(db: Session, experiment_id: int, experiment_update: ExperimentUpdate) -> Experiment:
    db_experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not db_experiment:
        return None
    for key, value in experiment_update.dict(exclude_unset=True).items():
        setattr(db_experiment, key, value)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment

def delete_experiment(db: Session, experiment_id: int) -> bool:
    db_experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not db_experiment:
        return False
    db.delete(db_experiment)
    db.commit()
    return True
