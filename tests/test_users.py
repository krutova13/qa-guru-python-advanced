from requests import Response

from app.models.models import UserData
from tests.conftest import (
    assert_response_ok,
    assert_response_not_found,
    assert_response_unprocessable_entity,
    validate_response_schema
)
from tests.schemas import USER_SCHEMA, USERS_LIST_SCHEMA


def test_create_user(api_client, create_user, valid_user):
    response: Response = create_user(valid_user)
    assert_response_ok(response)
    validate_response_schema(response, USER_SCHEMA)

    user = UserData.model_validate(response.json())
    assert user.name == valid_user["name"]
    assert user.surname == valid_user["surname"]
    assert user.birth_date == valid_user["birth_date"]


def test_get_all_users(api_client, create_user, valid_user):
    create_response: Response = create_user(valid_user)
    assert_response_ok(create_response)

    response: Response = api_client.get(f"{api_client.base_url}/users")
    assert_response_ok(response)
    validate_response_schema(response, USERS_LIST_SCHEMA)

    users = [UserData.model_validate(user) for user in response.json()]
    assert len(users) > 0
    assert any(user.id == valid_user["id"] for user in users)


def test_get_user_by_id(api_client, create_user, valid_user):
    create_response: Response = create_user(valid_user)
    assert_response_ok(create_response)

    response: Response = api_client.get(f"{api_client.base_url}/users/{valid_user['id']}")
    assert_response_ok(response)
    validate_response_schema(response, USER_SCHEMA)

    user = UserData.model_validate(response.json())
    assert user.id == valid_user["id"]
    assert user.name == valid_user["name"]


def test_get_nonexistent_user(api_client):
    response: Response = api_client.get(f"{api_client.base_url}/users/99999")
    assert_response_not_found(response)


def test_delete_user(api_client, create_user, valid_user):
    create_response: Response = create_user(valid_user)
    assert_response_ok(create_response)

    response: Response = api_client.delete(f"{api_client.base_url}/users/{valid_user['id']}")
    assert_response_ok(response)
    validate_response_schema(response, USER_SCHEMA)

    user = UserData.model_validate(response.json())
    assert user.id == valid_user["id"]

    get_response: Response = api_client.get(f"{api_client.base_url}/users/{valid_user['id']}")
    assert_response_not_found(get_response)


def test_create_user_invalid_data(api_client, create_user, invalid_user):
    response: Response = create_user(invalid_user)
    assert_response_unprocessable_entity(response)
