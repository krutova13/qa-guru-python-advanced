import os

import dotenv as dotenv
import pytest
import requests
from requests import Response

PREFIX = "/api/v1"


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()
    if not os.getenv("APP_URL"):
        raise ValueError(f"APP_URL не найден в .env файле")


@pytest.fixture(scope="function")
def api_client(envs):
    session = requests.Session()
    session.base_url = f"{os.getenv('APP_URL')}{PREFIX}"
    yield session
    session.close()


@pytest.fixture(scope="function", autouse=True)
def cleanup_database(api_client: requests.Session):
    yield

    for product in get_all_items(api_client, "products"):
        api_client.delete(f"{api_client.base_url}/products/{product['id']}")

    for user in get_all_items(api_client, "users"):
        api_client.delete(f"{api_client.base_url}/users/{user['id']}")


@pytest.fixture
def create_user(api_client: requests.Session):
    def _create_user(user_data: dict) -> Response:
        return api_client.post(f"{api_client.base_url}/users", json=user_data)

    return _create_user


@pytest.fixture
def create_product(api_client: requests.Session):
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


def get_all_items(api_client: requests.Session, endpoint: str) -> list:
    all_items = []
    page = 1
    while True:
        response = api_client.get(
            f"{api_client.base_url}/{endpoint}",
            params={"page": page, "size": 100}
        )
        data = response.json()
        all_items.extend(data["items"])

        if page >= data["pages"]:
            break
        page += 1
    return all_items
