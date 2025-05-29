import pytest
import requests
from jsonschema import validate
from requests import Response
from starlette import status

BASE_URL = "http://localhost:8000/api/v1"


@pytest.fixture(scope="function")
def api_client():
    session = requests.Session()
    session.base_url = BASE_URL
    yield session
    session.close()


@pytest.fixture(autouse=True)
def cleanup_database(api_client):
    yield

    products = api_client.get(f"{api_client.base_url}/products").json()
    for product in products:
        api_client.delete(f"{api_client.base_url}/products/{product['id']}")

    users = api_client.get(f"{api_client.base_url}/users").json()
    for user in users:
        api_client.delete(f"{api_client.base_url}/users/{user['id']}")


@pytest.fixture
def create_user(api_client):
    def _create_user(user_data: dict) -> Response:
        return api_client.post(f"{api_client.base_url}/users", json=user_data)

    return _create_user


@pytest.fixture
def create_product(api_client):
    def _create_product(product_data: dict) -> Response:
        return api_client.post(f"{api_client.base_url}/products", json=product_data)

    return _create_product


@pytest.fixture
def valid_user() -> dict:
    return {
        "id": 1,
        "name": "Test",
        "surname": "Testov",
        "birth_date": "01.10.1995",
        "products": []
    }


@pytest.fixture
def invalid_user() -> dict:
    return {
        "id": 2,
        "name": "Test",
        "surname": "Testov",
        "birth_date": "invalid-date",
        "products": []
    }


@pytest.fixture
def valid_product() -> dict:
    return {
        "id": 3,
        "title": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "user_id": 1
    }


def assert_response_ok(response: Response) -> None:
    assert response.status_code == status.HTTP_200_OK


def assert_response_not_found(response: Response) -> None:
    assert response.status_code == status.HTTP_404_NOT_FOUND


def assert_response_unprocessable_entity(response: Response) -> None:
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def validate_response_schema(response: Response, schema: dict) -> None:
    validate(instance=response.json(), schema=schema)
