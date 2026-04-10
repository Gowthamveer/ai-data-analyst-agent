from pydantic import BaseModel
from typing import Dict

class Observation(BaseModel):
    summary: str
    missing_values: int
    duplicates: int
    anomaly_count: int
    step_count: int

class Action(BaseModel):
    action_type: str
    payload: Dict
