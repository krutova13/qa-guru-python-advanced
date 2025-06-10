from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page

from app.api.dependencies import get_user_service, CustomParams
from app.core.decorators import handle_exceptions
from app.exceptions.exceptions import NotFoundException
from app.models.models import User, Product, UserCreate, UserUpdate
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
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise NotFoundException(f"Пользователь с id {user_id} не найден")
    return user


@handle_exceptions
@users_router.patch("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, user_service: UserService = Depends(get_user_service)):
    UserUpdate.model_validate(user_update.model_dump(mode="json"))
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise NotFoundException(f"Пользователь с id {user_id} не найден")
    updated_user = user_service.update_user(user_id, user_update)
    return updated_user


@handle_exceptions
@users_router.post("", response_model=User)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)) -> User:
    UserCreate.model_validate(user.model_dump(mode="json"))
    db_user = User(**user.dict())
    return user_service.create_user(db_user)


@handle_exceptions
@users_router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> User:
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise NotFoundException(f"Пользователь с id {user_id} не найден")
    user = user_service.delete_user(user_id)
    return user


@handle_exceptions
@users_router.get("/{user_id}/products", response_model=list[Product])
def get_user_products(user_id: int, user_service: UserService = Depends(get_user_service)) -> list[Product]:
    products = user_service.get_user_products(user_id)
    if not products:
        return []
    return products


@handle_exceptions
@users_router.get("/{user_id}/products/{product_id}", response_model=Product)
def get_user_product(user_id: int, product_id: int,
                     user_service: UserService = Depends(get_user_service)) -> Product:
    product = user_service.get_user_product(user_id, product_id)
    if not product:
        raise NotFoundException(f"Продукт не найден")
    return product
