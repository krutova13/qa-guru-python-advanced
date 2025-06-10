from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page

from app.api.dependencies import get_product_service, CustomParams
from app.core.decorators import handle_exceptions
from app.exceptions.exceptions import NotFoundException
from app.models.models import Product, ProductCreate
from app.services.product_service import ProductService

products_router = APIRouter(prefix="/products", tags=["products"])


@handle_exceptions
@products_router.get("", response_model=Page[Product])
def get_all_products(
        params: CustomParams = Depends(),
        product_service: ProductService = Depends(get_product_service)
) -> list[Product]:
    return paginate(product_service.get_products(), params)


@handle_exceptions
@products_router.get("/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, product_service: ProductService = Depends(get_product_service)) -> Product:
    if product := product_service.storage.get_by_id(product_id):
        return product
    raise NotFoundException(f"Продукт с id {product_id} не найден")


@handle_exceptions
@products_router.post("", response_model=Product)
def create_product(product: ProductCreate, product_service: ProductService = Depends(get_product_service)) -> Product:
    db_product = Product(**product.dict())
    return product_service.create_product(db_product)


@handle_exceptions
@products_router.delete("/{product_id}", response_model=Product)
def delete_product(product_id: int, product_service: ProductService = Depends(get_product_service)) -> Product:
    return product_service.delete_product(product_id)
