from fastapi import FastAPI

from api.routers import router

app = FastAPI(
    title="FastAPI Project",
    description="API для пользователей и их продуктов",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
