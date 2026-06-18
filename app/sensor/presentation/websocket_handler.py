import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.sensor.application.evaluate_alerts_use_case import EvaluateAlertsUseCase
from app.sensor.application.register_sensor_data import RegisterSensorDataUseCase
from app.sensor.infrastructure.mongodb.sensor_repository import MongoSensorRepository
from app.sensor.presentation.connection_manager import manager

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/sensor-data")
async def sensor_data_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    repo = MongoSensorRepository()
    use_case = RegisterSensorDataUseCase(repo)

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            logger.info("Sensor data: %s", data)

            reading = await use_case.execute(
                device_id=data.get("deviceId"),
                temperature=data.get("temperature"),
                humidity=data.get("humedad"),
                water_level=data.get("nivelAgua"),
            )

            await manager.broadcast(reading.to_dict())

            alerts_use_case = EvaluateAlertsUseCase()
            alerts = alerts_use_case.execute(
                temperature=reading.temperature,
                water_level=reading.water_level,
            )
            for alert in alerts:
                await manager.broadcast(alert)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception:
        logger.exception("Error in websocket handler")
    finally:
        manager.disconnect(websocket)
