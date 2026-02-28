from fastapi import FastAPI
from .module_loader import load_modules

app = FastAPI(title="MMS System")
load_modules(app)
