from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class SensorReading:
    id: str | None
    device_id: str
    temperature: float
    humidity: float
    water_level: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "device_id": self.device_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "water_level": self.water_level,
            "timestamp": self.timestamp.isoformat(),
        }


class SensorRepository(ABC):
    @abstractmethod
    async def save(self, reading: SensorReading) -> SensorReading:
        pass

    @abstractmethod
    async def get_latest(self, device_id: str, limit: int = 10) -> list[SensorReading]:
        pass

    @abstractmethod
    async def get_hourly_averages(
        self, device_id: str, hours: int = 24
    ) -> dict | None:
        pass
