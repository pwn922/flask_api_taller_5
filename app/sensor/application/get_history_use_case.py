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
        version_key = f"history_version:{device_id}"

        cached = await self.cache.get(cache_key)
        if cached is not None:
            current_version = await self.cache.get_int(version_key)
            if cached.get("version") == current_version:
                logger.info("Cache hit for %s (version %s)", cache_key, current_version)
                return cached["data"], True

        readings = await self.sensor_repository.get_latest(device_id, limit)
        data = [r.to_dict() for r in readings]

        if data:
            current_version = await self.cache.get_int(version_key) or 0
            await self.cache.set(
                cache_key,
                {"data": data, "version": current_version},
                ttl=10,
            )
        return data, False
