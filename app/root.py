from fastapi import FastAPI

import contextlib
from typing import AsyncIterator

from app.database.db import db_manager
from app import api


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_manager.init()
    yield
    await db_manager.close()


app = FastAPI(
    title="User registration API",
    lifespan=lifespan
)
app.include_router(
    api.router,
    prefix="/api/registration",
    tags=["users"]
)
