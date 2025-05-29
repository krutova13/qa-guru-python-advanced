from fastapi import APIRouter

from app.api.routers.products import products_router
from app.api.routers.users import users_router

router = APIRouter()

router.include_router(users_router)
router.include_router(products_router)


@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Это сервис Fast API"}
