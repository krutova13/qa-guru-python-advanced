from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page

from app.api.dependencies import get_user_service, CustomParams
from app.core.decorators import handle_exceptions
from app.exceptions.exceptions import NotFoundException
from app.models.user import User, Product
from app.services.user_service import UserService

users_router = APIRouter(prefix="/users", tags=["users"])


@handle_exceptions
@users_router.get("", response_model=Page[User])
def get_all_users(
        params: CustomParams = Depends(),
        user_service: UserService = Depends(get_user_service)
) -> list[User]:

    return paginate(user_service.get_users(), params)


@handle_exceptions
@users_router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)) -> User:
    if user := user_service.storage.get_by_id(user_id):
        return user
    raise NotFoundException(f"Пользователь с id {user_id} не найден")


@handle_exceptions
@users_router.post("", response_model=User)
def create_user(user: User, user_service: UserService = Depends(get_user_service)) -> User:
    return user_service.create_user(user)


@handle_exceptions
@users_router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> User:
    return user_service.delete_user(user_id)


@handle_exceptions
@users_router.get("/{user_id}/products", response_model=list[Product])
def get_user_products(user_id: int, user_service: UserService = Depends(get_user_service)) -> list[Product]:
    return user_service.get_user_products(user_id)


@handle_exceptions
@users_router.get("/{user_id}/products/{product_id}", response_model=Product)
def get_user_product(user_id: int, product_id: int,
                     user_service: UserService = Depends(get_user_service)) -> Product:
    return user_service.get_user_product(user_id, product_id)
