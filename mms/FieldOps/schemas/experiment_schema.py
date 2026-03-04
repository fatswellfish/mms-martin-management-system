from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExperimentBase(BaseModel):
    experiment_name: str
    batch_id: int
    vaccine_plan: str  # A, B, or C
    total_vaccine_doses: int
    target_population: int
    sample_size_1st: int
    sample_size_2nd: int
    status: str = "planning"


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentUpdate(BaseModel):
    vaccine_plan: Optional[str] = None
    total_vaccine_doses: Optional[int] = None
    target_population: Optional[int] = None
    sample_size_1st: Optional[int] = None
    sample_size_2nd: Optional[int] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ExperimentInDB(ExperimentBase):
    id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True
