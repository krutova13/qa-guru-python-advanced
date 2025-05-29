from fastapi import APIRouter, Depends

from app.api.dependencies import get_product_service
from app.core.decorators import handle_exceptions
from app.exceptions.exceptions import NotFoundException
from app.models.models import ProductData
from app.services.product_service import ProductService

products_router = APIRouter(prefix="/products", tags=["products"])


@handle_exceptions
@products_router.get("", response_model=list[ProductData])
def get_all_products(product_service: ProductService = Depends(get_product_service)) -> list[ProductData]:
    return product_service.get_products()


@handle_exceptions
@products_router.get("/{product_id}", response_model=ProductData)
def get_product_by_id(product_id: int, product_service: ProductService = Depends(get_product_service)) -> ProductData:
    if product := product_service.storage.get_by_id(product_id):
        return product
    raise NotFoundException(f"Продукт с id {product_id} не найден")


@handle_exceptions
@products_router.post("", response_model=ProductData)
def create_product(product: ProductData, product_service: ProductService = Depends(get_product_service)) -> ProductData:
    return product_service.create_product(product)


@handle_exceptions
@products_router.delete("/{product_id}", response_model=ProductData)
def delete_product(product_id: int, product_service: ProductService = Depends(get_product_service)) -> ProductData:
    return product_service.delete_product(product_id)
