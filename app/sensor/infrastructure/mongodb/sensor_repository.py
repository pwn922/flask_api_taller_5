from datetime import datetime

from app.db.mongodb.database import MongoDBConnection
from app.sensor.domain.sensor import SensorReading, SensorRepository


class MongoSensorRepository(SensorRepository):
    COLLECTION = "sensor_readings"

    async def save(self, reading: SensorReading) -> SensorReading:
        db = MongoDBConnection.get_db()
        doc = {
            "device_id": reading.device_id,
            "temperature": reading.temperature,
            "humidity": reading.humidity,
            "water_level": reading.water_level,
            "timestamp": reading.timestamp,
        }
        result = await db[self.COLLECTION].insert_one(doc)
        reading.id = str(result.inserted_id)
        return reading

    async def get_latest(self, device_id: str, limit: int = 10) -> list[SensorReading]:
        db = MongoDBConnection.get_db()
        cursor = (
            db[self.COLLECTION]
            .find({"device_id": device_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
        result = []
        async for doc in cursor:
            result.append(
                SensorReading(
                    id=str(doc["_id"]),
                    device_id=doc["device_id"],
                    temperature=doc["temperature"],
                    humidity=doc["humidity"],
                    water_level=doc["water_level"],
                    timestamp=doc["timestamp"],
                )
            )
        return result
