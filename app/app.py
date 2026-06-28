from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config
from app.common.logging import setup_logging
from app.db.mongodb.database import MongoDBConnection
from app.health.presentation.health_controller import router as health_router
from app.middleware.http_logging import HTTPLoggingMiddleware
from app.sensor.presentation.sensor_controller import router as sensor_router
from app.sensor.presentation.websocket_handler import router as ws_router
from app.sensor.presentation.sensor_ingest_controller import router as sensor_ingest_router

api_prefix = "/api"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await MongoDBConnection.connect()
    yield
    await MongoDBConnection.close()


def create_app() -> FastAPI:
    env = config.ENV
    setup_logging(env)

    app = FastAPI(
        title="Sensor API",
        debug=(env == "development"),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(HTTPLoggingMiddleware)

    app.include_router(health_router, prefix=f"{api_prefix}/health", tags=["health"])
    app.include_router(sensor_router)
    app.include_router(sensor_ingest_router)
    app.include_router(ws_router)

    
    return app


app = create_app()
