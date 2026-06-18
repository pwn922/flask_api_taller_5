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
        self, device_id: str, hours: int = 24
    ) -> tuple[dict | None, bool]:
        cache_key = f"averages:{device_id}:{hours}"
        cached = await self.cache.get(cache_key)
        if cached is not None:
            logger.info("Cache hit for %s", cache_key)
            return cached["result"], True

        result = await self.sensor_repository.get_hourly_averages(device_id, hours)
        if result is not None:
            await self.cache.set(cache_key, {"result": result}, ttl=30)
        return result, False
