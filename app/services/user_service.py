from app.models.models import User, Product
from app.models.models import UserUpdate
from app.services.product_service import ProductService
from app.storage.base_storage import BaseStorage


class UserService:
    def __init__(self, user_storage: BaseStorage, product_storage: BaseStorage):
        self.storage = user_storage
        self.product_storage = product_storage

    def create_user(self, user_data: User) -> User:
        return self.storage.save(user_data)

    def get_users(self) -> list[User]:
        return self.storage.get_all()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.storage.get_by_id(user_id)

    def update_user(self, user_id: int, user: UserUpdate):
        return self.storage.update(user_id, user)

    def delete_user(self, user_id: int) -> User | None:
        return self.storage.delete(user_id)

    def get_user_products(self, user_id: int) -> list[Product]:
        user = self.get_user_by_id(user_id)
        if not user:
            return []

        product_service = ProductService(self.product_storage)
        product = product_service.get_products_by_user_id(user_id)

        if not product:
            return []

        return product

    def get_user_product(self, user_id: int, product_id: int) -> Product | None:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        product_service = ProductService(self.product_storage)
        product = product_service.get_product_by_id(product_id)

        if not product or product.user_id != user_id:
            return None

        return product
