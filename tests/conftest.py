import os

import dotenv as dotenv
import pytest
import requests

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
def create_user(api_client: requests.Session, valid_user):
    api_client.post(f"{api_client.base_url}/users", json=valid_user)


@pytest.fixture
def create_product(api_client: requests.Session, valid_product):
    api_client.post(f"{api_client.base_url}/products", json=valid_product)


@pytest.fixture
def create_users(api_client, valid_user):
    _delete_items(api_client, "users")

    def _create(count):
        for _ in range(count):
            api_client.post(f"{api_client.base_url}/users", json=valid_user)

    return _create


@pytest.fixture
def create_products(api_client, valid_product):
    _delete_items(api_client, "products")

    def _create(count):
        for _ in range(count):
            api_client.post(f"{api_client.base_url}/products", json=valid_product)

    return _create


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


def _delete_items(api_client: requests.Session, endpoint: str):
    response = api_client.get(f"{api_client.base_url}/{endpoint}")
    items = response.json()["items"]
    if items:
        for item in items:
            api_client.delete(f"{api_client.base_url}/{endpoint}/{item['id']}")
