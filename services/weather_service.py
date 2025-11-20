import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import AsyncSessionLocal  # Import the sessionmaker
from services.data_service import create_wind_data, create_solar_data
from schemas.wind import WindCreate
from schemas.solar import SolarCreate
import os
from dotenv import load_dotenv

load_dotenv()

LAT = float(os.getenv("API_LOCATION_LAT", 40.7128)) 
LON = float(os.getenv("API_LOCATION_LON", -74.0060))  

WIND_POWER_FACTOR = 0.0005 
SOLAR_EFFICIENCY_FACTOR = 0.0002  
USAGE_FACTOR_WIND = 0.6
USAGE_FACTOR_SOLAR = 0.7

async def fetch_and_store_weather_data():
    db: AsyncSession = AsyncSessionLocal() 
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
           
            url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true&hourly=shortwave_radiation&timezone=auto"
            response = await client.get(url)
            if response.status_code != 200:
                raise ValueError(f"API request failed: {response.status_code}")
            
            data = response.json()
            current = data.get("current_weather", {})
            hourly = data.get("hourly", {})
            
            if not current or not hourly:
                raise ValueError("Invalid API response")
            
            # Wind data
            wind_speed_kmh = current.get("windspeed", 0)
            wind_speed_ms = wind_speed_kmh / 3.6  # Convert to m/s
            wind_direction = current.get("winddirection", 0)
            temperature = current.get("temperature", 0)
            current_generated_wind = WIND_POWER_FACTOR * (wind_speed_ms ** 3)
            current_used_wind = current_generated_wind * USAGE_FACTOR_WIND
            
            if "shortwave_radiation" in hourly and hourly["shortwave_radiation"]:
                sunlight_irradiance = hourly["shortwave_radiation"][-1]  
                sunlight_irradiance = 0
            current_generated_solar = sunlight_irradiance * SOLAR_EFFICIENCY_FACTOR
            current_used_solar = current_generated_solar * USAGE_FACTOR_SOLAR
            wind_create = WindCreate(
                wind_speed=wind_speed_ms,
                wind_direction=wind_direction,
                temperature=temperature,
                current_generated=current_generated_wind,
                current_used=current_used_wind
            )
            await create_wind_data(db, wind_create)
            solar_create = SolarCreate(
                sunlight_irradiance=sunlight_irradiance,
                temperature=temperature,
                current_generated=current_generated_solar,
                current_used=current_used_solar
            )
            await create_solar_data(db, solar_create)
            
            await db.commit()
            print(f"Stored weather data: Wind speed {wind_speed_ms:.2f} m/s, Irradiance {sunlight_irradiance} W/m²")
    
    except Exception as e:
        await db.rollback()
        print(f"Weather service error: {e}")
    finally:
        await db.close()
