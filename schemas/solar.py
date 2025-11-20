 add from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SolarCreate(BaseModel):
    sunlight_irradiance: float
    temperature: Optional[float] = None
    current_generated: Optional[float] = None
    current_used: Optional[float] = None

class SolarResponse(BaseModel):
    id: int
    timestamp: datetime
    sunlight_irradiance: float
    temperature: Optional[float]
    current_generated: float
    current_used: float

    class Config:
        from_attributes = True
