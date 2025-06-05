from app.models.user import Product
from app.storage.base_storage import BaseStorage


class ProductService:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def create_product(self, product_data: Product) -> Product:
        return self.storage.save(product_data)

    def get_products(self) -> list[Product]:
        return self.storage.get()

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.storage.get_by_id(product_id)

    def get_products_by_user_id(self, user_id: int) -> list[Product]:
        all_products = self.get_products()
        return [product for product in all_products if product.user_id == user_id]

    def delete_product(self, product_id: int) -> Product | None:
        return self.storage.delete(product_id)
