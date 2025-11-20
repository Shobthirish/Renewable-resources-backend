from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import uvicorn
from db.database import engine
from routers import data, websocket
from models.base import Base

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Renewable Energy Backend (Sim Only)", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/api")
app.include_router(websocket.router, prefix="/ws")

@app.get("/")
def read_root():
    return {"message": "Application Started"}

# Run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
