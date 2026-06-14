import contextlib
import logging
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Client connected: %s", websocket.client)

    def disconnect(self, websocket: WebSocket):
        with contextlib.suppress(ValueError):
            self.active_connections.remove(websocket)
        logger.info("Client disconnected: %s", websocket.client)

    async def broadcast(self, data: dict[str, Any]):
        for connection in self.active_connections:
            with contextlib.suppress(WebSocketDisconnect, RuntimeError):
                await connection.send_json(data)


manager = ConnectionManager()
