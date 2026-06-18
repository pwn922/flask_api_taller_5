from datetime import datetime, timedelta, timezone

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

        return [
            SensorReading(
                id=str(doc["_id"]),
                device_id=doc["device_id"],
                temperature=doc["temperature"],
                humidity=doc["humidity"],
                water_level=doc["water_level"],
                timestamp=doc["timestamp"],
            )
            async for doc in cursor
        ]

    async def get_hourly_averages(self, device_id: str, hours: int = 24) -> dict | None:
        db = MongoDBConnection.get_db()
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        pipeline = [
            {"$match": {"device_id": device_id, "timestamp": {"$gte": since}}},
            {
                "$group": {
                    "_id": None,
                    "first_timestamp": {"$min": "$timestamp"},
                    "last_timestamp": {"$max": "$timestamp"},
                    "avg_temperature": {"$avg": "$temperature"},
                    "avg_humidity": {"$avg": "$humidity"},
                    "avg_water_level": {"$avg": "$water_level"},
                    "samples": {"$sum": 1},
                },
            },
            {
                "$project": {
                    "_id": 0,
                    "first_timestamp": 1,
                    "last_timestamp": 1,
                    "avg_temperature": {"$round": ["$avg_temperature", 1]},
                    "avg_humidity": {"$round": ["$avg_humidity", 1]},
                    "avg_water_level": {"$round": ["$avg_water_level", 1]},
                    "samples": 1,
                },
            },
        ]
        cursor = db[self.COLLECTION].aggregate(pipeline)
        docs = await cursor.to_list(length=1)
        if not docs:
            return None
        result = docs[0]
        result["first_timestamp"] = result["first_timestamp"].isoformat()
        result["last_timestamp"] = result["last_timestamp"].isoformat()
        return result
