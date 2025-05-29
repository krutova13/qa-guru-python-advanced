from fastapi import Depends

from app.models.models import UserData, ProductData
from app.services.product_service import ProductService
from app.services.user_service import UserService
from app.storage.base_storage import BaseStorage
from app.storage.factory import StorageFactory


def get_user_storage() -> BaseStorage[UserData]:
    return StorageFactory.get_storage(model_type=UserData)


def get_product_storage() -> BaseStorage[ProductData]:
    return StorageFactory.get_storage(model_type=ProductData)


def get_user_service(
        storage: BaseStorage[UserData] = Depends(get_user_storage),
        product_storage: BaseStorage[ProductData] = Depends(get_product_storage)
) -> UserService:
    return UserService(storage, product_storage)


def get_product_service(storage: BaseStorage[ProductData] = Depends(get_product_storage)) -> ProductService:
    return ProductService(storage)
