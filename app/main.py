import os

import dotenv

dotenv.load_dotenv()

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.storage.database_engine import create_db_and_tables

from app.api.routers import router

app = FastAPI(
    title="FastAPI Project",
    description="API для пользователей и их продуктов",
    version="1.0.0"
)
add_pagination(app)
app.include_router(router, prefix="/api/v1")

create_db_and_tables()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT"))
    )
