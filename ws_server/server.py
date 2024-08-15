import websockets

from ws_server.data import ConnectedClients
from ws_server.config import LoggingWS
from ws_server.config import Settings

import asyncio
import logging


logging.basicConfig(level=logging.INFO)


class WebsocketServer:
    def __init__(self):
        self.logging_ws = LoggingWS()
        self.connected_clients = ConnectedClients.clients
        self.settings = Settings()

    async def broadcast(self, message):
        for client in self.connected_clients:
            await client.send(message)

    async def ws_server_handler(self, websocket):
        self.connected_clients.append(websocket)
        while True:
            try:
                message = await websocket.recv()
                logging.info(f"{self.logging_ws.received_message}{message}")
                await self.broadcast(message=message)
            except Exception as _ex:
                logging.warning(_ex)
                self.connected_clients.remove(websocket)
                break

    async def start(self):
        async with websockets.serve(
                self.ws_server_handler,
                host=self.settings.HOST,
                port=self.settings.PORT
        ):
            await asyncio.Future()
