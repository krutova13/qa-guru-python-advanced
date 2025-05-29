from app.models.models import UserData, ProductData
from app.services.product_service import ProductService
from app.storage.base_storage import BaseStorage


class UserService:
    def __init__(self, storage: BaseStorage, product_storage: BaseStorage):
        self.storage = storage
        self.product_storage = product_storage

    def create_user(self, user_data: UserData) -> UserData:
        return self.storage.save(user_data)

    def get_users(self) -> list[UserData]:
        users = self.storage.get()
        for user in users:
            self._load_user_products(user)
        return users

    def get_user_by_id(self, user_id: int) -> UserData | None:
        user = self.storage.get_by_id(user_id)
        if user:
            self._load_user_products(user)
        return user

    def delete_user(self, user_id: int) -> UserData | None:
        return self.storage.delete(user_id)

    def get_user_products(self, user_id: int) -> list[ProductData]:
        user = self.get_user_by_id(user_id)
        if not user:
            return []
        return user.products

    def get_user_product(self, user_id: int, product_id: int) -> ProductData | None:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        product_service = ProductService(self.product_storage)
        product = product_service.get_product_by_id(product_id)

        if not product or product.user_id != user_id:
            return None

        return product

    def _load_user_products(self, user: UserData) -> None:
        product_service = ProductService(self.product_storage)
        user.products = product_service.get_products_by_user_id(user.id)
