from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.database import get_db
from schemas.wind import WindCreate, WindResponse
from schemas.solar import SolarCreate, SolarResponse
from schemas.sim_data import SimDataCreate
from models.wind import WindTurbineData
from models.solar import SolarPanelData
from services.data_service import create_wind_data, create_solar_data, get_recent_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/wind-data", response_model=WindResponse)
async def add_wind_data(wind_input: WindCreate, db: AsyncSession = Depends(get_db)):
    if wind_input.current_generated is None:
        wind_input.current_generated = 0.000245 * (wind_input.wind_speed ** 3)  # kW
    if wind_input.current_used is None:
        wind_input.current_used = wind_input.current_generated * 0.7  # 70% used
    db_wind = WindTurbineData(**wind_input.dict())
    created = await create_wind_data(db, db_wind)
    logger.info(f"Wind data inserted: speed={wind_input.wind_speed}, generated={wind_input.current_generated}")
    return created

@router.post("/solar-data", response_model=SolarResponse)
async def add_solar_data(solar_input: SolarCreate, db: AsyncSession = Depends(get_db)):
    if solar_input.current_generated is None:
        solar_input.current_generated = solar_input.sunlight_irradiance * 0.00024  # kW for 1m² panel
    if solar_input.current_used is None:
        solar_input.current_used = solar_input.current_generated * 0.7
    db_solar = SolarPanelData(**solar_input.dict())
    created = await create_solar_data(db, db_solar)
    logger.info(f"Solar data inserted: irradiance={solar_input.sunlight_irradiance}, generated={solar_input.current_generated}")
    return created

@router.post("/sim-data")
async def add_sim_data(sim_data: SimDataCreate, db: AsyncSession = Depends(get_db)):
    wind_resp = await add_wind_data(sim_data.wind, db)
    solar_resp = await add_solar_data(sim_data.solar, db)
    return {"wind": wind_resp, "solar": solar_resp}

@router.get("/recent-data")
async def get_recent_combined(db: AsyncSession = Depends(get_db)):
    return await get_recent_data(db)
