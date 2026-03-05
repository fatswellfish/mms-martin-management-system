"""
Experiment API Router

This module defines the FastAPI routes for the experiment system in FieldOps.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from .database import get_db_session
from .experiment_service import service

# Create router instance
router = APIRouter(prefix="/FieldOps/api", tags=["experiment"])

# Request models
class RunExperimentRequest(BaseModel):
    experiment_id: str
    batch_ids: List[str]

# Response models
class ExperimentResponse(BaseModel):
    experiment_id: str
    name: str
    status: str
    created_at: str
    updated_at: str
    scenarios: List[dict]

class RunExperimentResponse(BaseModel):
    success: bool
    recommendation: dict
    results: List[dict]

@router.get("/experiment", response_model=List[ExperimentResponse])
async def get_active_experiments():
    """Get all active experiments with their scenarios"""
    try:
        # Get database session
        db_session = get_db_session()
        
        # Get active experiments
        experiments = service.get_active_experiments()
        
        # Convert to response model
        return experiments
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving experiments: {e}")

@router.post("/experiment/run", response_model=RunExperimentResponse)
async def run_experiment(request: RunExperimentRequest):
    """Run an experiment on a list of batches and return recommendation results"""
    try:
        # Get database session
        db_session = get_db_session()
        
        # Run the experiment
        result = service.run_experiment(
            experiment_id=request.experiment_id,
            batch_ids=request.batch_ids
        )
        
        # Return result
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running experiment: {e}")