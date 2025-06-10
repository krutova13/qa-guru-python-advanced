from typing import Iterable

from app.models.models import Product, ProductCreate
from app.storage.database.database_storage import DatabaseStorage


class ProductStorage(DatabaseStorage):

    def __init__(self):
        super().__init__(model_type=Product)

    def save(self, product: ProductCreate) -> Product:
        return super().save(product)

    def get_all(self) -> Iterable[Product]:
        return super().get_all()

    def get_by_id(self, product_id: int) -> Product | None:
        return super().get_by_id(product_id)

    def update(self, product: Product, product_id: int) -> Product | None:
        return super().update(product, product_id)

    def delete(self, product_id: int) -> Product | None:
        return super().delete(product_id)
