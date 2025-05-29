from requests import Response

from app.models.models import ProductData
from tests.conftest import (
    assert_response_ok,
    assert_response_not_found,
    validate_response_schema,
)
from tests.schemas import PRODUCT_SCHEMA, PRODUCTS_LIST_SCHEMA


def test_create_product(api_client, create_product, valid_product):
    create_response: Response = create_product(valid_product)
    assert_response_ok(create_response)

    response: Response = api_client.post(f"{api_client.base_url}/products", json=valid_product)
    assert_response_ok(response)
    validate_response_schema(response, PRODUCT_SCHEMA)

    product = ProductData.model_validate(response.json())
    assert product.title == valid_product["title"]
    assert product.description == valid_product["description"]
    assert product.price == valid_product["price"]
    assert product.user_id == valid_product["user_id"]


def test_get_all_products(api_client, create_product, valid_product):
    create_response: Response = create_product(valid_product)
    assert_response_ok(create_response)

    response: Response = api_client.get(f"{api_client.base_url}/products")
    assert_response_ok(response)
    validate_response_schema(response, PRODUCTS_LIST_SCHEMA)

    products = [ProductData.model_validate(product) for product in response.json()]
    assert len(products) > 0
    assert any(product.id == valid_product["id"] for product in products)


def test_get_product_by_id(api_client, create_product, valid_product):
    create_response: Response = create_product(valid_product)
    assert_response_ok(create_response)

    response: Response = api_client.get(f"{api_client.base_url}/products/{valid_product['id']}")
    assert_response_ok(response)
    validate_response_schema(response, PRODUCT_SCHEMA)

    product = ProductData.model_validate(response.json())
    assert product.id == valid_product["id"]
    assert product.title == valid_product["title"]


def test_get_nonexistent_product(api_client):
    response: Response = api_client.get(f"{api_client.base_url}/products/99999")
    assert_response_not_found(response)


def test_delete_product(api_client, create_product, valid_product):
    create_response: Response = create_product(valid_product)
    assert_response_ok(create_response)

    response: Response = api_client.delete(f"{api_client.base_url}/products/{valid_product['id']}")
    assert_response_ok(response)
    validate_response_schema(response, PRODUCT_SCHEMA)

    product = ProductData.model_validate(response.json())
    assert product.id == valid_product["id"]

    get_response: Response = api_client.get(f"{api_client.base_url}/products/{valid_product['id']}")
    assert_response_not_found(get_response)


def test_get_user_products(api_client, create_user, create_product, valid_user, valid_product):
    create_user_response: Response = create_user(valid_user)
    assert_response_ok(create_user_response)

    create_product_response: Response = create_product(valid_product)
    assert_response_ok(create_product_response)

    response: Response = api_client.get(f"{api_client.base_url}/users/{valid_product['user_id']}/products")
    assert_response_ok(response)
    validate_response_schema(response, PRODUCTS_LIST_SCHEMA)

    products = [ProductData.model_validate(product) for product in response.json()]
    assert len(products) > 0
    assert any(product.id == valid_product["id"] for product in products)


def test_get_user_product(api_client, create_user, create_product, valid_user, valid_product):
    create_user_response: Response = create_user(valid_user)
    assert_response_ok(create_user_response)

    create_product_response: Response = create_product(valid_product)
    assert_response_ok(create_product_response)

    response: Response = api_client.get(
        f"{api_client.base_url}/users/{valid_user['id']}/products/{valid_product['id']}"
    )
    assert_response_ok(response)
    validate_response_schema(response, PRODUCT_SCHEMA)

    product = ProductData.model_validate(response.json())
    assert product.id == valid_product["id"]
    assert product.title == valid_product["title"]
