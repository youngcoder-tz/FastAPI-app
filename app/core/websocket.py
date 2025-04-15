from fastapi import WebSocket
from collections import defaultdict
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(dict)
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str, channel: str):
        await websocket.accept()
        async with self.lock:
            self.active_connections[channel][user_id] = websocket

    async def disconnect(self, user_id: str, channel: str):
        async with self.lock:
            self.active_connections[channel].pop(user_id, None)

    async def broadcast(self, message: dict, channel: str):
        async with self.lock:
            for connection in self.active_connections[channel].values():
                await connection.send_json(message)

    async def send_personal(self, user_id: str, message: dict, channel: str):
        async with self.lock:
            if conn := self.active_connections[channel].get(user_id):
                await conn.send_json(message)

ws_manager = ConnectionManager()