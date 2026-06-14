import os

from dotenv import load_dotenv

load_dotenv()

ENV = os.environ.get("FLASK_ENV", "development").lower()


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret123")
    DEBUG = False
    TESTING = False

    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
    REDIS_CACHE_TTL = int(os.environ.get("REDIS_CACHE_TTL", "300"))

    MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/sensor_db")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "sensor_db")


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

ActiveConfig = config.get(ENV, DevelopmentConfig)
