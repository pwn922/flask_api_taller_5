import logging

from fastapi import APIRouter, status

from app.common.dependencies import get_redis_cache
from app.sensor.application.evaluate_alerts_use_case import EvaluateAlertsUseCase
from app.sensor.application.register_sensor_data import RegisterSensorDataUseCase
from app.sensor.infrastructure.mongodb.sensor_repository import MongoSensorRepository
from app.sensor.presentation.connection_manager import manager
from app.sensor.presentation.schemas import SensorDataRequest

logger = logging.getLogger(__name__)

router = APIRouter(tags=["sensor-ingest"])

LATEST_STATE_TTL_SECONDS = 30


@router.post("/sensor-data", status_code=status.HTTP_201_CREATED)
async def ingest_sensor_data(payload: SensorDataRequest):
    repo = MongoSensorRepository()
    cache = get_redis_cache()

    register_use_case = RegisterSensorDataUseCase(repo)

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

    alerts_use_case = EvaluateAlertsUseCase()
    alerts = alerts_use_case.execute(
        temperature=reading.temperature,
        water_level=reading.water_level,
    )

    for alert in alerts:
        await manager.broadcast(alert)

    logger.info(
        "Sensor data ingested by POST | device=%s temp=%.1f hum=%.1f water=%.1f",
        reading.device_id,
        reading.temperature,
        reading.humidity,
        reading.water_level,
    )

    return {
        "message": "Sensor data received",
        "device_id": reading.device_id,
        "data": reading_data,
        "alerts": alerts,
        "cached_latest": True,
    }