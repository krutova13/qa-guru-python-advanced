import os
from contextlib import asynccontextmanager

import dotenv

dotenv.load_dotenv()

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.storage.database_engine import create_db_and_tables

from app.api.routers import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="FastAPI Project",
    description="API для пользователей и их продуктов",
    version="1.0.0",
    lifespan=lifespan
)

add_pagination(app)
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT"))
    )
