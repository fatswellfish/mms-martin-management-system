from fastapi import FastAPI
from mms.mms_agent_farm_loader import load_farm_modules

app = FastAPI(title="FARM Standalone System")

load_farm_modules(app)

