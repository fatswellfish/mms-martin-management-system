# mms/fieldops/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class Farm(BaseModel):
    id: int
    name: str

class Barn(BaseModel):
    id: int
    name: str
    farm_id: int

class Pen(BaseModel):
    id: int
    name: str
    barn_id: int

class FarmWithBarns(BaseModel):
    id: int
    name: str
    barns: List[Barn]

class BarnWithPens(BaseModel):
    id: int
    name: str
    pens: List[Pen]