import logging

from app.common.cache.redis_cache import RedisCache
from app.sensor.domain.sensor import SensorRepository

logger = logging.getLogger(__name__)


class GetHourlyAveragesUseCase:
    def __init__(
        self,
        sensor_repository: SensorRepository,
        cache: RedisCache,
    ):
        self.sensor_repository = sensor_repository
        self.cache = cache

    async def execute(
        self,
        device_id: str,
        hours: int = 24,
    ) -> tuple[dict | None, bool]:
        cache_key = f"averages:{device_id}:{hours}"
        version_key = f"averages_version:{device_id}"

        cached = await self.cache.get(cache_key)
        if cached is not None:
            current_version = await self.cache.get_int(version_key)
            if cached.get("version") == current_version:
                logger.info("Cache hit for %s (version %s)", cache_key, current_version)
                return cached["result"], True

        result = await self.sensor_repository.get_hourly_averages(device_id, hours)
        if result is not None:
            current_version = await self.cache.get_int(version_key) or 0
            await self.cache.set(
                cache_key,
                {"result": result, "version": current_version},
                ttl=30,
            )
        return result, False
