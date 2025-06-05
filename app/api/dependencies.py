from fastapi import Depends
from fastapi_pagination import Params

from app.models.user import User, Product
from app.services.product_service import ProductService
from app.services.user_service import UserService
from app.storage.base_storage import BaseStorage
from app.storage.factory import StorageFactory


class CustomParams(Params):
    size: int = 10
    max_size: int = 50


def get_user_storage() -> BaseStorage[User]:
    return StorageFactory.get_storage(model_type=User)


def get_product_storage() -> BaseStorage[Product]:
    return StorageFactory.get_storage(model_type=Product)


def get_user_service(
        storage: BaseStorage[User] = Depends(get_user_storage),
        product_storage: BaseStorage[Product] = Depends(get_product_storage)
) -> UserService:
    return UserService(storage, product_storage)


def get_product_service(storage: BaseStorage[Product] = Depends(get_product_storage)) -> ProductService:
    return ProductService(storage)
