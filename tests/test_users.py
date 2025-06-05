from http import HTTPStatus
from typing import List

import pytest as pytest
from requests import Response

from app.models.user import User
from tests.test_helpers import validate_paginated_response


def test_create_user(api_client, valid_user: dict):
    create_response: Response = api_client.post(f"{api_client.base_url}/users", json=valid_user)
    assert create_response.status_code == HTTPStatus.OK

    user = User.model_validate(create_response.json())
    assert user.name == valid_user["name"]
    assert user.surname == valid_user["surname"]
    assert user.birth_date == valid_user["birth_date"]

    response: Response = api_client.get(f"{api_client.base_url}/users/{valid_user['id']}")
    assert response.status_code == HTTPStatus.OK


def test_get_all_users(api_client, create_user, valid_user: dict):
    create_response: Response = create_user(valid_user)
    assert create_response.status_code == HTTPStatus.OK

    response: Response = api_client.get(f"{api_client.base_url}/users")
    assert response.status_code == HTTPStatus.OK

    users: List[User] = [User.model_validate(user) for user in response.json()]
    assert len(users) > 0
    assert any(user.id == valid_user["id"] for user in users)


def test_get_user_by_id(api_client, create_user, valid_user: dict):
    create_response: Response = create_user(valid_user)
    assert create_response.status_code == HTTPStatus.OK

    response: Response = api_client.get(f"{api_client.base_url}/users/{valid_user['id']}")
    assert response.status_code == HTTPStatus.OK

    user = User.model_validate(response.json())
    assert user.id == valid_user["id"]
    assert user.name == valid_user["name"]


def test_get_nonexistent_user(api_client):
    response: Response = api_client.get(f"{api_client.base_url}/users/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(api_client, create_user, valid_user: dict):
    create_response: Response = create_user(valid_user)
    assert create_response.status_code == HTTPStatus.OK

    response: Response = api_client.delete(f"{api_client.base_url}/users/{valid_user['id']}")
    assert response.status_code == HTTPStatus.OK

    user = User.model_validate(response.json())
    assert user.id == valid_user["id"]

    get_response: Response = api_client.get(f"{api_client.base_url}/users/{valid_user['id']}")
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
def test_pagination(api_client, create_user, valid_user, total_users, page, size):
    for _ in range(total_users):
        create_user(valid_user)

    response: Response = api_client.get(f"{api_client.base_url}/users?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    validate_paginated_response(data, page, size, total_users)
