"""
Experiment Models

This module defines the data models for the experiment system in FieldOps.
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Experiment(Base):
    """Model representing an experiment (vaccine scenario comparison)"""
    
    __tablename__ = 'experiments'
    
    # Primary key
    experiment_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic information
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="active")  # active, paused, completed
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to scenarios
    scenarios = relationship("Scenario", back_populates="experiment", cascade="all, delete-orphan")
    
    def to_dict(self) -> dict:
        """Convert experiment instance to dictionary"""
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Scenario(Base):
    """Model representing a scenario within an experiment"""
    
    __tablename__ = 'scenarios'
    
    # Primary key
    scenario_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign key to experiment
    experiment_id = Column(String(36), ForeignKey('experiments.experiment_id'), nullable=False)
    
    # Basic information
    name = Column(String(255), nullable=False)
    parameters = Column(JSON, nullable=False)  # JSON field for configuration parameters
    priority = Column(Integer, nullable=False, default=1)  # Priority from 1-10
    
    # Relationship to experiment
    experiment = relationship("Experiment", back_populates="scenarios")
    
    def to_dict(self) -> dict:
        """Convert scenario instance to dictionary"""
        return {
            "scenario_id": self.scenario_id,
            "experiment_id": self.experiment_id,
            "name": self.name,
            "parameters": self.parameters,
            "priority": self.priority
        }