import math
from http import HTTPStatus

import pytest as pytest
import requests as requests
from requests import Response

from app.models.models import Product
from tests.test_helpers import validate_paginated_response


def test_create_product(api_client, valid_product: dict, create_user):
    valid_product["user_id"] = create_user.id

    create_response: Response = api_client.post(f"{api_client.base_url}/products", json=valid_product)
    assert create_response.status_code == HTTPStatus.OK

    product = Product.model_validate(create_response.json())
    assert product.title == valid_product["title"]
    assert product.description == valid_product["description"]
    assert product.price == valid_product["price"]
    assert product.user_id == create_user.id

    response = api_client.get(f"{api_client.base_url}/products/{product.id}")
    assert response.status_code == HTTPStatus.OK


def test_get_all_products(api_client, create_product):
    response: Response = api_client.get(f"{api_client.base_url}/products")
    assert response.status_code == HTTPStatus.OK

    products: list[Product] = [Product.model_validate(product) for product in response.json()["items"]]
    assert len(products) > 0
    assert any(create_product.id == product.id for product in products)


def test_get_product_by_id(api_client, create_product):
    response: Response = api_client.get(f"{api_client.base_url}/products/{create_product.id}")
    assert response.status_code == HTTPStatus.OK

    product = Product.model_validate(response.json())
    assert create_product.id == product.id
    assert create_product.title == product.title


def test_get_nonexistent_product(api_client):
    response: Response = api_client.get(f"{api_client.base_url}/products/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_product(api_client, create_product):
    response: Response = api_client.delete(f"{api_client.base_url}/products/{create_product.id}")
    assert response.status_code == HTTPStatus.OK

    product = Product.model_validate(response.json())
    assert create_product.id == product.id

    get_response = api_client.get(f"{api_client.base_url}/products/{product.id}")
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_get_user_products(api_client, create_product):
    response: Response = api_client.get(f"{api_client.base_url}/users/{create_product.user_id}/products")
    assert response.status_code == HTTPStatus.OK

    products: list[Product] = [Product.model_validate(product) for product in response.json()]
    assert len(products) > 0
    assert any(create_product.id == product.id for product in products)


def test_get_user_product(api_client: requests.Session, create_user, create_product):
    response: Response = api_client.get(
        f"{api_client.base_url}/users/{create_user.id}/products/{create_product.id}"
    )
    assert response.status_code == HTTPStatus.OK

    product = Product.model_validate(response.json())
    assert product.id == create_product.id
    assert product.title == create_product.title


@pytest.mark.parametrize("total_products, page, size", [
    (1, 1, 10),
    (10, 1, 10),
    (11, 1, 10),
    (11, 2, 10),
    (30, 3, 10),
    (5, 1, 1),
])
def test_pagination(api_client, create_products, total_products, page, size):
    create_products(total_products)

    response: Response = api_client.get(f"{api_client.base_url}/products?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    validate_paginated_response(data, page, size, total_products)


@pytest.mark.parametrize("size", [1, 5, 10, 15, 16])
def test_pagination_valid_products_count(api_client, create_products, size: int):
    total_products: int = 15
    create_products(total_products)

    total_pages = math.ceil(total_products / size)

    response = api_client.get(f"{api_client.base_url}/products?size={size}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["pages"] == total_pages


def test_pagination_page_switch(api_client, create_products):
    total_products: int = 15
    page1: int = 1
    page2: int = 2
    size: int = 10

    create_products(total_products)

    response1: Response = api_client.get(f"{api_client.base_url}/products?page={page1}&size={size}")
    response2: Response = api_client.get(f"{api_client.base_url}/products?page={page2}&size={size}")

    assert response1.status_code == HTTPStatus.OK
    assert response2.status_code == HTTPStatus.OK

    items1 = response1.json()["items"]
    items2 = response2.json()["items"]

    assert items1 != items2
