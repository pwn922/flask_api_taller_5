import logging

from fastapi import APIRouter, Depends, Query

from app.common.cache.redis_cache import RedisCache
from app.common.dependencies import get_redis_cache, get_sensor_repository
from app.sensor.application.get_history_use_case import GetHistoryUseCase
from app.sensor.application.get_hourly_averages_use_case import GetHourlyAveragesUseCase
from app.sensor.domain.sensor import SensorRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/sensor", tags=["sensor"])


@router.get("/{device_id}/latest")
async def get_latest_state(
    device_id: str,
    cache: RedisCache = Depends(get_redis_cache),
):
    latest = await cache.get(f"latest:{device_id}")

    if latest is None:
        return {
            "device_id": device_id,
            "online": False,
            "data": None,
            "cached": False,
            "message": "No recent sensor state found",
        }

    return {
        "device_id": device_id,
        "online": True,
        "data": latest.get("data"),
        "cached": True,
    }


@router.get("/{device_id}/history")
async def get_history(
    device_id: str,
    limit: int = Query(default=10, ge=1, le=100),
    repo: SensorRepository = Depends(get_sensor_repository),
    cache: RedisCache = Depends(get_redis_cache),
):
    use_case = GetHistoryUseCase(repo, cache)
    data, cached = await use_case.execute(device_id, limit)
    return {
        "device_id": device_id,
        "samples": len(data),
        "data": data,
        "cached": cached,
    }


@router.get("/{device_id}/averages")
async def get_hourly_averages(
    device_id: str,
    hours: int = Query(default=24, ge=1, le=168),
    repo: SensorRepository = Depends(get_sensor_repository),
    cache: RedisCache = Depends(get_redis_cache),
):
    use_case = GetHourlyAveragesUseCase(repo, cache)
    result, cached = await use_case.execute(device_id, hours)
    if result is None:
        return {
            "device_id": device_id,
            "hours": hours,
            "samples": 0,
            "cached": cached,
        }
    return {
        "device_id": device_id,
        "hours": hours,
        **result,
        "cached": cached,
    }
