import json
import logging

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.common.cache.redis_cache import RedisCache
from app.common.dependencies import get_redis_cache, get_sensor_repository
from app.sensor.application.evaluate_alerts_use_case import EvaluateAlertsUseCase
from app.sensor.application.register_sensor_data import RegisterSensorDataUseCase
from app.sensor.domain.sensor import SensorRepository
from app.sensor.presentation.connection_manager import manager
from app.sensor.presentation.schemas import SensorDataRequest

logger = logging.getLogger(__name__)

router = APIRouter()

LATEST_STATE_TTL_SECONDS = 30


@router.websocket("/sensor-data")
async def sensor_data_websocket(
    websocket: WebSocket,
    repo: SensorRepository = Depends(get_sensor_repository),
    cache: RedisCache = Depends(get_redis_cache),
):
    await manager.connect(websocket)

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
                    },
                )
                continue
            except ValidationError as error:
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Invalid sensor data payload",
                        "details": error.errors(),
                    },
                )
                continue

            reading = await register_use_case.execute(
                device_id=payload.device_id,
                temperature=payload.temperature,
                humidity=payload.humidity,
                water_level=payload.water_level,
            )

            reading_data = reading.to_dict()

            await cache.set(
                f"latest:{reading.device_id}",
                {"data": reading_data},
                ttl=LATEST_STATE_TTL_SECONDS,
            )

            await cache.incr(f"history_version:{reading.device_id}")
            await cache.incr(f"averages_version:{reading.device_id}")

            alerts = alerts_use_case.execute(
                temperature=reading.temperature,
                water_level=reading.water_level,
                device_id=reading.device_id,
            )

            await manager.broadcast(
                {
                    "type": "sensor_event",
                    "data": reading_data,
                    "alerts": alerts,
                },
            )

    except WebSocketDisconnect:
        logger.info("Client disconnected")

    except Exception:
        logger.exception("Error in websocket handler")

    finally:
        manager.disconnect(websocket)
