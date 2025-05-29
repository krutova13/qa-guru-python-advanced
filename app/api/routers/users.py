from fastapi import APIRouter, Depends

from app.api.dependencies import get_user_service
from app.core.decorators import handle_exceptions
from app.exceptions.exceptions import NotFoundException
from app.models.models import UserData, ProductData
from app.services.user_service import UserService

users_router = APIRouter(prefix="/users", tags=["users"])


@handle_exceptions
@users_router.get("", response_model=list[UserData])
def get_all_users(user_service: UserService = Depends(get_user_service)) -> list[UserData]:
    return user_service.get_users()


@handle_exceptions
@users_router.get("/{user_id}", response_model=UserData)
def get_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)) -> UserData:
    if user := user_service.storage.get_by_id(user_id):
        return user
    raise NotFoundException(f"Пользователь с id {user_id} не найден")


@handle_exceptions
@users_router.post("", response_model=UserData)
def create_user(user: UserData, user_service: UserService = Depends(get_user_service)) -> UserData:
    return user_service.create_user(user)


@handle_exceptions
@users_router.delete("/{user_id}", response_model=UserData)
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> UserData:
    return user_service.delete_user(user_id)


@handle_exceptions
@users_router.get("/{user_id}/products", response_model=list[ProductData])
def get_user_products(user_id: int, user_service: UserService = Depends(get_user_service)) -> list[ProductData]:
    return user_service.get_user_products(user_id)


@handle_exceptions
@users_router.get("/{user_id}/products/{product_id}", response_model=ProductData)
def get_user_product(user_id: int, product_id: int,
                     user_service: UserService = Depends(get_user_service)) -> ProductData:
    return user_service.get_user_product(user_id, product_id)
