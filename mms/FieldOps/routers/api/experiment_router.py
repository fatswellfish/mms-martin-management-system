from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from mms.FieldOps.database import get_db
from mms.FieldOps.models.experiment import Experiment
from mms.FieldOps.schemas.experiment_schema import ExperimentCreate, ExperimentUpdate, ExperimentInDB
from mms.FieldOps.services.experiment_service import (
    get_experiment,
    get_experiments,
    create_experiment,
    update_experiment,
    delete_experiment
)

router = APIRouter(
    prefix="/api/experiments",
    tags=["experiments"]
)

@router.get("/")
async def read_experiments(skip: int = Query(0), limit: int = Query(100), db: Session = Depends(get_db)):
    experiments = get_experiments(db, skip=skip, limit=limit)
    return [exp.to_dict() for exp in experiments]

@router.get("/{experiment_id}")
async def read_experiment(experiment_id: int, db: Session = Depends(get_db)):
    experiment = get_experiment(db, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment.to_dict()

@router.post("/")
async def create_new_experiment(experiment: ExperimentCreate, db: Session = Depends(get_db)):
    db_experiment = create_experiment(db, experiment)
    return db_experiment.to_dict()

@router.put("/{experiment_id}")
async def update_existing_experiment(experiment_id: int, experiment_update: ExperimentUpdate, db: Session = Depends(get_db)):
    updated_experiment = update_experiment(db, experiment_id, experiment_update)
    if not updated_experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return updated_experiment.to_dict()

@router.delete("/{experiment_id}")
async def delete_experiment_item(experiment_id: int, db: Session = Depends(get_db)):
    success = delete_experiment(db, experiment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"message": "Experiment deleted successfully"}
