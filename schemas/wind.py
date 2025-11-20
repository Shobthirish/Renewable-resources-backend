from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WindCreate(BaseModel):
    wind_speed: float
    wind_direction: float
    temperature: Optional[float] = None
    current_generated: Optional[float] = None
    current_used: Optional[float] = None

class WindResponse(BaseModel):
    id: int
    timestamp: datetime
    wind_speed: float
    wind_direction: float
    temperature: Optional[float]
    current_generated: float
    current_used: float

    class Config:
        from_attributes = True
