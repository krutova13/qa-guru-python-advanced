from http import HTTPStatus

import pytest as pytest
import requests as requests
from requests import Response

from app.models.product import Product
from tests.test_helpers import validate_paginated_response


def test_create_product(api_client, valid_product: dict):
    create_response: Response = api_client.post(f"{api_client.base_url}/products", json=valid_product)
    assert create_response.status_code == HTTPStatus.OK

    product = Product.model_validate(create_response.json())
    assert product.title == valid_product["title"]
    assert product.description == valid_product["description"]
    assert product.price == valid_product["price"]
    assert product.user_id == valid_product["user_id"]

    get_response: Response = api_client.get(f"{api_client.base_url}/products/{valid_product['id']}")
    assert get_response.status_code == HTTPStatus.OK


def test_get_all_products(api_client, create_product, valid_product: dict):
    create_response: Response = create_product(valid_product)
    assert create_response.status_code == HTTPStatus.OK

    response: Response = api_client.get(f"{api_client.base_url}/products")
    assert response.status_code == HTTPStatus.OK

    products = [Product.model_validate(product) for product in response.json()]
    assert len(products) > 0
    assert any(product.id == valid_product["id"] for product in products)


def test_get_product_by_id(api_client, create_product, valid_product: dict):
    create_response: Response = create_product(valid_product)
    assert create_response.status_code == HTTPStatus.OK

    response: Response = api_client.get(f"{api_client.base_url}/products/{valid_product['id']}")
    assert response.status_code == HTTPStatus.OK

    product = Product.model_validate(response.json())
    assert product.id == valid_product["id"]
    assert product.title == valid_product["title"]


def test_get_nonexistent_product(api_client):
    response: Response = api_client.get(f"{api_client.base_url}/products/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_product(api_client, create_product, valid_product: dict):
    create_response: Response = create_product(valid_product)
    assert create_response.status_code == HTTPStatus.OK

    response: Response = api_client.delete(f"{api_client.base_url}/products/{valid_product['id']}")
    assert response.status_code == HTTPStatus.OK

    product = Product.model_validate(response.json())
    assert product.id == valid_product["id"]

    get_response: Response = api_client.get(f"{api_client.base_url}/products/{valid_product['id']}")
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_get_user_products(api_client, create_user, create_product, valid_user: dict, valid_product: dict) -> None:
    create_user_response: Response = create_user(valid_user)
    assert create_user_response.status_code == HTTPStatus.OK

    create_product_response: Response = create_product(valid_product)
    assert create_product_response.status_code == HTTPStatus.OK

    response: Response = api_client.get(f"{api_client.base_url}/users/{valid_product['user_id']}/products")
    assert response.status_code == HTTPStatus.OK

    products: list[Product] = [Product.model_validate(product) for product in response.json()]
    assert len(products) > 0
    assert any(product.id == valid_product["id"] for product in products)


def test_get_user_product(api_client: requests.Session, create_user, create_product, valid_user: dict,
                          valid_product: dict):
    create_user_response: Response = create_user(valid_user)
    assert create_user_response.status_code == HTTPStatus.OK

    create_product_response: Response = create_product(valid_product)
    assert create_product_response.status_code == HTTPStatus.OK

    response: Response = api_client.get(
        f"{api_client.base_url}/users/{valid_user['id']}/products/{valid_product['id']}"
    )
    assert response.status_code == HTTPStatus.OK

    product = Product.model_validate(response.json())
    assert product.id == valid_product["id"]
    assert product.title == valid_product["title"]


@pytest.mark.parametrize("total_products, page, size", [
    (1, 1, 10),
    (10, 1, 10),
    (11, 1, 10),
    (11, 2, 10),
    (30, 3, 10),
    (5, 1, 1),
])
def test_pagination(api_client, create_product, valid_product, total_products, page, size):
    for _ in range(total_products):
        create_product(valid_product)

    response: Response = api_client.get(f"{api_client.base_url}/products?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    validate_paginated_response(data, page, size, total_products)
