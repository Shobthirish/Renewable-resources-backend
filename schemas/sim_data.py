from pydantic import BaseModel
from .wind import WindCreate
from .solar import SolarCreate
class SimDataCreate(BaseModel):
    wind: WindCreate
    solar: SolarCreate
