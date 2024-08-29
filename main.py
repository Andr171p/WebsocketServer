import uvicorn

from app.root import app
from app.server.config import network


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=network.host,
        port=network.port
    )
