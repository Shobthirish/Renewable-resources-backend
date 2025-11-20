from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.wind import WindTurbineData
from models.solar import SolarPanelData
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

async def create_wind_data(db: AsyncSession, wind_data: WindTurbineData):
    db.add(wind_data)
    await db.commit()
    await db.refresh(wind_data)
    # Fill nulls post-insert if still null (edge case)
    if wind_data.current_generated is None:
        wind_data.current_generated = 0.0
    if wind_data.current_used is None:
        wind_data.current_used = 0.0
    await db.commit()
    return wind_data

async def create_solar_data(db: AsyncSession, solar_data: SolarPanelData):
    db.add(solar_data)
    await db.commit()
    await db.refresh(solar_data)
    if solar_data.current_generated is None:
        solar_data.current_generated = 0.0
    if solar_data.current_used is None:
        solar_data.current_used = 0.0
    await db.commit()
    return solar_data

async def get_recent_data(db: AsyncSession, limit: int = 10) -> Dict[str, List]:
    result_wind = await db.execute(select(WindTurbineData).order_by(WindTurbineData.timestamp.desc()).limit(limit))
    wind = result_wind.scalars().all()
    result_solar = await db.execute(select(SolarPanelData).order_by(SolarPanelData.timestamp.desc()).limit(limit))
    solar = result_solar.scalars().all()
    return {"winds": [w.__dict__ for w in wind], "solars": [s.__dict__ for s in solar]}
