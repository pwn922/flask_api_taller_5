from app.sensor.domain.sensor import SensorRepository


class GetDevicesUseCase:
    def __init__(self, sensor_repository: SensorRepository):
        self.sensor_repository = sensor_repository

    async def execute(self) -> list[dict]:
        return await self.sensor_repository.get_devices()
