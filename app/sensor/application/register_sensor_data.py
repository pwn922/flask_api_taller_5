import logging

from app.sensor.domain.sensor import SensorReading, SensorRepository

logger = logging.getLogger(__name__)


class RegisterSensorDataUseCase:
    def __init__(self, sensor_repository: SensorRepository):
        self.sensor_repository = sensor_repository

    async def execute(
        self,
        device_id: str,
        temperature: float,
        humidity: float,
        water_level: float,
    ) -> SensorReading:
        reading = SensorReading(
            id=None,
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            water_level=water_level,
        )
        saved = await self.sensor_repository.save(reading)
        logger.info(
            "Sensor data saved | device=%s temp=%.1f hum=%.1f water=%.1f",
            device_id,
            temperature,
            humidity,
            water_level,
        )
        return saved
