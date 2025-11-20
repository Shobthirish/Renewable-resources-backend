from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from .base import Base

class WindTurbineData(Base):
    __tablename__ = "wind_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    wind_speed = Column(Float, nullable=False)  
    wind_direction = Column(Float, nullable=False)  
    temperature = Column(Float, nullable=True)  
    current_generated = Column(Float, nullable=True)  
    current_used = Column(Float, nullable=True)  
