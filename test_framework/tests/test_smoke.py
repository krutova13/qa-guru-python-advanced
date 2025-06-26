from http import HTTPStatus

from requests import Response

from app.models.models import User, UserUpdate
from test_framework.clients.api_client import ApiClient
from test_framework.clients.user_client import UsersApiClient


def test_status(env: str):
    response = ApiClient(env).request(method="GET", url="/status")
    assert response.status_code == HTTPStatus.OK


def test_user_flow(env: str, valid_user: User):
    create_response: Response = UsersApiClient(env).create_user(valid_user.model_dump())
    assert create_response.status_code == HTTPStatus.OK
    created_user = User.model_validate(create_response.json())

    get_response: Response = UsersApiClient(env).get_user_by_id(created_user.id)
    assert get_response.status_code == HTTPStatus.OK
    get_user = User.model_validate(get_response.json())

    update_data = get_user.model_dump()
    update_data.pop("id")
    update_data["name"] = "Updated"

    update_response: Response = UsersApiClient(env).update_user(get_user.id, UserUpdate.model_validate(update_data))
    assert update_response.status_code == HTTPStatus.OK
    updated_user = User.model_validate(update_response.json())

    delete_response: Response = UsersApiClient(env).delete_user(updated_user.id)
    assert delete_response.status_code == HTTPStatus.OK
    deleted_user = User.model_validate(delete_response.json())

    assert created_user.id == deleted_user.id
    assert updated_user.name == deleted_user.name
