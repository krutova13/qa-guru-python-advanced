from http import HTTPStatus

from requests import Response

from app.models.models import User


def test_status(api_client):
    response = api_client.get(f"{api_client.base_url}/status")
    assert response.status_code == HTTPStatus.OK


def test_user_flow(api_client, valid_user):
    create_response: Response = api_client.post(f"{api_client.base_url}/users", json=valid_user)
    assert create_response.status_code == HTTPStatus.OK
    created_user = User.model_validate(create_response.json())

    get_response: Response = api_client.get(f"{api_client.base_url}/users/{created_user.id}")
    assert get_response.status_code == HTTPStatus.OK
    get_user = User.model_validate(get_response.json())

    update_data = get_user.model_dump()
    update_data.pop("id")
    update_data["name"] = "Updated"

    update_response: Response = api_client.patch(f"{api_client.base_url}/users/{get_user.id}", json=update_data)
    assert update_response.status_code == HTTPStatus.OK
    updated_user = User.model_validate(update_response.json())

    delete_response: Response = api_client.delete(f"{api_client.base_url}/users/{updated_user.id}")
    assert delete_response.status_code == HTTPStatus.OK
    deleted_user = User.model_validate(delete_response.json())

    assert created_user.id == deleted_user.id
    assert updated_user.name == deleted_user.name
