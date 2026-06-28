import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.common.dependencies import get_redis_cache
from app.sensor.application.evaluate_alerts_use_case import EvaluateAlertsUseCase
from app.sensor.application.register_sensor_data import RegisterSensorDataUseCase
from app.sensor.infrastructure.mongodb.sensor_repository import MongoSensorRepository
from app.sensor.presentation.connection_manager import manager
from app.sensor.presentation.schemas import SensorDataRequest

logger = logging.getLogger(__name__)

router = APIRouter()

LATEST_STATE_TTL_SECONDS = 30


@router.websocket("/sensor-data")
async def sensor_data_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    repo = MongoSensorRepository()
    cache = get_redis_cache()
    register_use_case = RegisterSensorDataUseCase(repo)
    alerts_use_case = EvaluateAlertsUseCase()

    try:
        while True:
            raw = await websocket.receive_text()

            try:
                data = json.loads(raw)
                payload = SensorDataRequest.model_validate(data)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid JSON format",
                    }
                )
                continue
            except ValidationError as error:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid sensor data payload",
                        "details": error.errors(),
                    }
                )
                continue

            logger.info("Sensor data received by WebSocket: %s", data)

            reading = await register_use_case.execute(
                device_id=payload.device_id,
                temperature=payload.temperature,
                humidity=payload.humidity,
                water_level=payload.water_level,
            )

            reading_data = reading.to_dict()

            latest_key = f"latest:{reading.device_id}"
            await cache.set(
                latest_key,
                {"data": reading_data},
                ttl=LATEST_STATE_TTL_SECONDS,
            )

            await cache.delete_pattern(f"history:{reading.device_id}:*")
            await cache.delete_pattern(f"averages:{reading.device_id}:*")

            await manager.broadcast(reading_data)

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