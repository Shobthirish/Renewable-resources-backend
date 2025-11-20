import asyncio
from datetime import datetime, timedelta
import random
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from models.solar import SolarPanelData
from models.wind import WindTurbineData

async def generate_mock_data(db: AsyncSession):
    # Generate mock solar data
    solar_data = []
    base_time = datetime.utcnow() - timedelta(days=1)
    for i in range(100):
        timestamp = base_time + timedelta(minutes=i*15)  # Every 15 minutes
        sunlight_irradiance = random.uniform(0, 1000)  # W/m²
        temperature = random.uniform(-10, 50)  # °C
        current_generated = random.uniform(0, 50)  # A
        current_used = random.uniform(0, current_generated)  # A, less than generated
        solar_data.append(SolarPanelData(
            timestamp=timestamp,
            sunlight_irradiance=sunlight_irradiance,
            temperature=temperature,
            current_generated=current_generated,
            current_used=current_used
        ))

    # Generate mock wind data
    wind_data = []
    for i in range(100):
        timestamp = base_time + timedelta(minutes=i*15)
        wind_speed = random.uniform(0, 20)  # m/s
        wind_direction = random.uniform(0, 360)  # degrees
        temperature = random.uniform(-10, 30)  # °C
        current_generated = random.uniform(0, 40)  # A
        current_used = random.uniform(0, current_generated)  # A
        wind_data.append(WindTurbineData(
            timestamp=timestamp,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            temperature=temperature,
            current_generated=current_generated,
            current_used=current_used
        ))

    # Insert data
    db.add_all(solar_data + wind_data)
    await db.commit()
    print("Mock data inserted successfully!")

async def main():
    async for db in get_db():
        await generate_mock_data(db)
        break

if __name__ == "__main__":
    asyncio.run(main())
