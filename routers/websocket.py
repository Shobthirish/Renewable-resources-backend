from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from services.data_service import get_recent_data
import json
import asyncio

router = APIRouter()

@router.websocket("/data")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            recent_data = await get_recent_data(db)
            await websocket.send_text(json.dumps(recent_data))
            await asyncio.sleep(10)  # Every 10s for viz updates
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
