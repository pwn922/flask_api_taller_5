from app.common.cache.redis_cache import RedisCache

_redis_cache = RedisCache()


def get_redis_cache() -> RedisCache:
    return _redis_cache
