import logging

from fastapi import APIRouter, Depends, status

from app.common.cache.redis_cache import RedisCache
from app.common.dependencies import get_redis_cache, get_sensor_repository
from app.sensor.application.evaluate_alerts_use_case import EvaluateAlertsUseCase
from app.sensor.application.register_sensor_data import RegisterSensorDataUseCase
from app.sensor.domain.sensor import SensorRepository
from app.sensor.presentation.connection_manager import manager
from app.sensor.presentation.schemas import SensorDataRequest

logger = logging.getLogger(__name__)

router = APIRouter(tags=["sensor-ingest"])

LATEST_STATE_TTL_SECONDS = 30


@router.post("/sensor-data", status_code=status.HTTP_201_CREATED)
async def ingest_sensor_data(
    payload: SensorDataRequest,
    repo: SensorRepository = Depends(get_sensor_repository),
    cache: RedisCache = Depends(get_redis_cache),
):
    register_use_case = RegisterSensorDataUseCase(repo)
    alerts_use_case = EvaluateAlertsUseCase()

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

    await manager.broadcast(
        {
            "type": "reading",
            "data": reading_data,
        },
    )

    alerts = alerts_use_case.execute(
        temperature=reading.temperature,
        water_level=reading.water_level,
    )

    if alerts:
        await manager.broadcast(
            {
                "type": "alerts",
                "data": alerts,
            },
        )

    logger.info(
        "Sensor data ingested | device=%s temp=%.1f hum=%.1f water=%.1f",
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
