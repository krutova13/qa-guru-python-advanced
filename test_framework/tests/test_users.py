import math
from http import HTTPStatus

import pytest as pytest
from requests import Response

from app.models.models import User, Product, UserCreate, UserUpdate
from test_framework.clients.user_client import UsersApiClient
from test_framework.tests.test_helpers import validate_paginated_response


def test_create_user(valid_user: UserCreate, users_api):
    create_response: Response = users_api.create_user(valid_user.model_dump())
    assert create_response.status_code == HTTPStatus.OK

    user: User = User.model_validate(create_response.json())
    assert user.name == valid_user.name
    assert user.surname == valid_user.surname
    assert user.birth_date == valid_user.birth_date

    response = users_api.get_user_by_id(user.id)
    assert response.status_code == HTTPStatus.OK


def test_get_all_users(create_user: User, cleanup_database, users_api):
    response: Response = users_api.get_all_users()
    assert response.status_code == HTTPStatus.OK

    users: list[User] = [User.model_validate(user) for user in response.json()["items"]]
    assert len(users) > 0
    assert any(create_user.id == user.id for user in users)


def test_get_user_by_id(create_user: User, users_api):
    response: Response = users_api.get_user_by_id(create_user.id)
    assert response.status_code == HTTPStatus.OK

    user: User = User.model_validate(response.json())
    assert create_user.id == user.id
    assert create_user.name == user.name


def test_update_user_by_id(create_user: User, users_api):
    get_response: Response = users_api.get_user_by_id(create_user.id)
    assert get_response.status_code == HTTPStatus.OK
    update_user: UserUpdate = UserUpdate(
        name="Nastya",
        surname="Artemova",
        birth_date="16.10.1995",
        products=[]
    )

    update_response: Response = users_api.update_user(create_user.id, user_update=update_user)
    assert get_response.status_code == HTTPStatus.OK

    up_user: User = User.model_validate(update_response.json())
    assert create_user.id == up_user.id
    assert update_user.name == up_user.name
    assert update_user.surname == up_user.surname

    response: Response = users_api.get_user_by_id(create_user.id)
    assert get_response.status_code == HTTPStatus.OK

    user: User = User.model_validate(response.json())
    assert update_user.name == user.name
    assert update_user.surname == user.surname


def test_get_nonexistent_user(users_api):
    response: Response = users_api.get_user_by_id(99999)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_nonexistent_user(users_api):
    response: Response = users_api.delete_user(99999)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_nonexistent_user(users_api):
    update_user: UserUpdate = UserUpdate(
        name="Nastya",
        surname="Artemova",
        birth_date="16.10.1995",
        products=[]
    )
    response: Response = users_api.update_user(99999, update_user)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(env: str, create_user: User):
    response: Response = UsersApiClient(env).delete_user(create_user.id)
    assert response.status_code == HTTPStatus.OK

    user = User.model_validate(response.json())
    assert create_user.id == user.id

    get_response = UsersApiClient(env).get_user_by_id(user.id)
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_create_user_invalid_data(env: str, invalid_user: dict):
    response: Response = UsersApiClient(env).create_user(invalid_user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_user_products(env: str, create_product: Product):
    response: Response = UsersApiClient(env).get_user_products(create_product.user_id)
    assert response.status_code == HTTPStatus.OK

    products: list[Product] = [Product.model_validate(product) for product in response.json()]
    assert len(products) > 0
    assert any(create_product.id == product.id for product in products)


def test_get_user_product(env: str, create_user: User, create_product: Product):
    response: Response = UsersApiClient(env).get_user_product(create_user.id, create_product.id)
    assert response.status_code == HTTPStatus.OK

    product = Product.model_validate(response.json())
    assert product.id == create_product.id
    assert product.title == create_product.title


@pytest.mark.parametrize("total_users, page, size", [
    (1, 1, 10),
    (10, 1, 10),
    (11, 1, 10),
    (11, 2, 10),
    (30, 3, 10),
    (5, 1, 1),
])
def test_pagination_valid_items_count(env: str, create_users, total_users: int, page: int, size: int):
    create_users(total_users)
    params: dict = {"page": page, "size": size}
    response: Response = UsersApiClient(env).request("GET", "/users", params=params)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    validate_paginated_response(data, page, size, total_users)


@pytest.mark.parametrize("size", [1, 5, 10, 15, 16])
def test_pagination_valid_pages_count(env: str, create_users, size: int):
    total_users: int = 15
    create_users(total_users)

    total_pages = math.ceil(total_users / size)

    response = UsersApiClient(env).request("GET", "/users", params={"size": size})

    assert response.status_code == HTTPStatus.OK
    assert response.json()["pages"] == total_pages


def test_pagination_page_switch(env: str, create_users):
    total_users: int = 15
    page1: int = 1
    page2: int = 2
    size: int = 10

    create_users(total_users)
    params1: dict = {"page": page1, "size": size}
    params2: dict = {"page": page2, "size": size}

    response1: Response = UsersApiClient(env).request("GET", "/users", params=params1)
    response2: Response = UsersApiClient(env).request("GET", "/users", params=params2)

    assert response1.status_code == HTTPStatus.OK
    assert response2.status_code == HTTPStatus.OK

    items1 = response1.json()["items"]
    items2 = response2.json()["items"]

    assert items1 != items2
