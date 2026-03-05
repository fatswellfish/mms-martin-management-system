"""
API Package Initialization

This file initializes the API package for the FieldOps project.
"""

# Import key routers
from .experiment_router import router as experiment_router

# Define what gets imported with "from api import *"
__all__ = [
    "experiment_router"
]

# Package metadata
__version__ = "1.0.0"
__author__ = "OpenClaw Assistant"
__description__ = "API routes for the FieldOps project"