import math
from http import HTTPStatus

import pytest as pytest
from requests import Response

from app.models.models import User
from tests.test_helpers import validate_paginated_response


def test_create_user(api_client, valid_user: dict):
    create_response: Response = api_client.post(f"{api_client.base_url}/users", json=valid_user)
    assert create_response.status_code == HTTPStatus.OK

    user = User.model_validate(create_response.json())
    assert user.name == valid_user["name"]
    assert user.surname == valid_user["surname"]
    assert user.birth_date == valid_user["birth_date"]

    response = api_client.get(f"{api_client.base_url}/users/{user.id}")
    assert response.status_code == HTTPStatus.OK


def test_get_all_users(api_client, create_user: User):
    response: Response = api_client.get(f"{api_client.base_url}/users")
    assert response.status_code == HTTPStatus.OK

    users: list[User] = [User.model_validate(user) for user in response.json()["items"]]
    assert len(users) > 0
    assert any(create_user.id == user.id for user in users)


def test_get_user_by_id(api_client, create_user: User):
    response: Response = api_client.get(f"{api_client.base_url}/users/{create_user.id}")
    assert response.status_code == HTTPStatus.OK

    user: User = User.model_validate(response.json())
    assert create_user.id == user.id
    assert create_user.name == user.name


def test_update_user_by_id(api_client, create_user: User):
    get_response: Response = api_client.get(f"{api_client.base_url}/users/{create_user.id}")
    assert get_response.status_code == HTTPStatus.OK
    update_user = {
        "name": "Nastya",
        "surname": "Artemova",
        "birth_date": "16.10.1995",
        "products": []
    }

    update_response: Response = api_client.patch(f"{api_client.base_url}/users/{create_user.id}", json=update_user)
    assert get_response.status_code == HTTPStatus.OK

    up_user: User = User.model_validate(update_response.json())
    assert create_user.id == up_user.id
    assert update_user.get("name") == up_user.name
    assert update_user.get("surname") == up_user.surname

    response: Response = api_client.get(f"{api_client.base_url}/users/{create_user.id}")
    assert get_response.status_code == HTTPStatus.OK

    user: User = User.model_validate(response.json())
    assert update_user.get("name") == user.name
    assert update_user.get("surname") == user.surname


def test_get_nonexistent_user(api_client):
    response: Response = api_client.get(f"{api_client.base_url}/users/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_nonexistent_user(api_client):
    response: Response = api_client.delete(f"{api_client.base_url}/users/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_nonexistent_user(api_client, valid_user):
    response: Response = api_client.patch(f"{api_client.base_url}/users/99999", json=valid_user)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(api_client, create_user: User):
    response: Response = api_client.delete(f"{api_client.base_url}/users/{create_user.id}")
    assert response.status_code == HTTPStatus.OK

    user = User.model_validate(response.json())
    assert create_user.id == user.id

    get_response = api_client.get(f"{api_client.base_url}/users/{user.id}")
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_create_user_invalid_data(api_client, invalid_user: dict):
    response: Response = api_client.post(f"{api_client.base_url}/users", json=invalid_user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("total_users, page, size", [
    (1, 1, 10),
    (10, 1, 10),
    (11, 1, 10),
    (11, 2, 10),
    (30, 3, 10),
    (5, 1, 1),
])
def test_pagination_valid_items_count(api_client, create_users, total_users, page, size):
    create_users(total_users)

    response: Response = api_client.get(f"{api_client.base_url}/users?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    validate_paginated_response(data, page, size, total_users)


@pytest.mark.parametrize("size", [1, 5, 10, 15, 16])
def test_pagination_valid_pages_count(api_client, create_users, size: int):
    total_users: int = 15
    create_users(total_users)

    total_pages = math.ceil(total_users / size)

    response = api_client.get(f"{api_client.base_url}/users?size={size}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["pages"] == total_pages


def test_pagination_page_switch(api_client, create_users):
    total_users: int = 15
    page1: int = 1
    page2: int = 2
    size: int = 10

    create_users(total_users)

    response1: Response = api_client.get(f"{api_client.base_url}/users?page={page1}&size={size}")
    response2: Response = api_client.get(f"{api_client.base_url}/users?page={page2}&size={size}")

    assert response1.status_code == HTTPStatus.OK
    assert response2.status_code == HTTPStatus.OK

    items1 = response1.json()["items"]
    items2 = response2.json()["items"]

    assert items1 != items2
