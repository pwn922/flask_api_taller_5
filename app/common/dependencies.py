from app.sensor.domain.sensor import SensorRepository
from app.sensor.infrastructure.mongodb.sensor_repository import MongoSensorRepository

from app.common.cache.redis_cache import RedisCache

_redis_cache = RedisCache()


def get_redis_cache() -> RedisCache:
    return _redis_cache


def get_sensor_repository() -> SensorRepository:
    return MongoSensorRepository()
