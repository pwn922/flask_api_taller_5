import json
from collections.abc import Mapping
from typing import Any

import redis.asyncio as redis

from app import config


class RedisCache:
    def __init__(self):
        self._client: redis.Redis | None = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.Redis(
                host=config.ActiveConfig.REDIS_HOST,
                port=config.ActiveConfig.REDIS_PORT,
                password=config.ActiveConfig.REDIS_PASSWORD,
                decode_responses=True,
            )
        return self._client

    async def get(self, key: str) -> dict[str, Any] | None:
        data = await self.client.get(key)
        if data is not None:
            return json.loads(data)
        return None

    async def set(self, key: str, value: Mapping[str, Any], ttl: int | None) -> None:
        """
        Guarda un valor serializable como JSON en Redis.
        `value` puede ser dict, TypedDict, etc.
        """
        ttl = ttl or config.ActiveConfig.REDIS_CACHE_TTL
        await self.client.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        cursor = 0
        while True:
            cursor, keys = await self.client.scan(
                cursor=cursor,
                match=pattern,
                count=100,
            )
            if keys:
                await self.client.delete(*keys)
            if cursor == 0:
                break

    async def get_int(self, key: str) -> int | None:
        value = await self.client.get(key)
        if value is not None:
            return int(value)
        return None

    async def incr(self, key: str) -> int:
        return await self.client.incr(key)
