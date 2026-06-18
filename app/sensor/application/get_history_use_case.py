import logging

from app.common.cache.redis_cache import RedisCache
from app.sensor.domain.sensor import SensorRepository

logger = logging.getLogger(__name__)


class GetHistoryUseCase:
    def __init__(
        self,
        sensor_repository: SensorRepository,
        cache: RedisCache,
    ):
        self.sensor_repository = sensor_repository
        self.cache = cache

    async def execute(self, device_id: str, limit: int = 10) -> tuple[list[dict], bool]:
        cache_key = f"history:{device_id}:{limit}"
        cached = await self.cache.get(cache_key)
        if cached is not None:
            logger.info("Cache hit for %s", cache_key)
            return cached["data"], True

        readings = await self.sensor_repository.get_latest(device_id, limit)
        data = [r.to_dict() for r in readings]

        if data:
            await self.cache.set(cache_key, {"data": data}, ttl=10)
        return data, False
