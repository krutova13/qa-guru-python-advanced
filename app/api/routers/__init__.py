from http import HTTPStatus

from fastapi import APIRouter

from app.api.routers.products import products_router
from app.api.routers.users import users_router
from app.models.app_status import AppStatus
from app.storage.database_engine import check_availability

router = APIRouter()

router.include_router(users_router)
router.include_router(products_router)


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=check_availability())
