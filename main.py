import asyncio

from ws_server.server import WebsocketServer


websocket_server = WebsocketServer()


if __name__ == '__main__':
    asyncio.run(websocket_server.start())
