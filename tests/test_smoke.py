from http import HTTPStatus


def test_status(api_client):
    response = api_client.get(f"{api_client.base_url}/status")
    assert response.status_code == HTTPStatus.OK
