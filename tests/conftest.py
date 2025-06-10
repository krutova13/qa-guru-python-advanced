import os

import dotenv as dotenv
import pytest
import requests
from sqlmodel import Session, create_engine

from app.models.models import User, Product

PREFIX = "/api/v1"


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


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
def cleanup_database():
    yield
    engine = get_test_engine()
    with Session(engine) as session:
        session.query(Product).delete()
        session.query(User).delete()
        session.commit()


@pytest.fixture
def create_user(api_client: requests.Session, valid_user: dict) -> User:
    response = api_client.post(f"{api_client.base_url}/users", json=valid_user)
    return User(**response.json())


@pytest.fixture
def create_product(api_client: requests.Session, valid_product: dict, create_user: User) -> Product:
    product_data = valid_product.copy()
    product_data["user_id"] = create_user.id
    response = api_client.post(f"{api_client.base_url}/products", json=product_data)
    return Product(**response.json())


@pytest.fixture
def create_users(api_client, valid_user):
    _delete_items(api_client, "users")

    def _create(count):
        for _ in range(count):
            user_data = valid_user.copy()
            api_client.post(f"{api_client.base_url}/users", json=user_data)

    return _create


@pytest.fixture
def create_products(api_client, valid_product, create_user):
    _delete_items(api_client, "products")

    def _create(count):
        for _ in range(count):
            product_data = valid_product.copy()
            product_data["user_id"] = create_user.id
            api_client.post(f"{api_client.base_url}/products", json=product_data)

    return _create


@pytest.fixture
def valid_user() -> dict:
    return {
        "name": "Test",
        "surname": "Testov",
        "birth_date": "01.10.1995",
        "products": []
    }


@pytest.fixture
def invalid_user() -> dict:
    return {
        "name": "Test",
        "surname": "Testov",
        "birth_date": "invalid-date",
        "products": []
    }


@pytest.fixture
def valid_product() -> dict:
    return {
        "title": "Test Product",
        "description": "Test Description",
        "price": 100.0
    }


def get_test_engine():
    database_engine = os.getenv("DATABASE_ENGINE")
    if not database_engine:
        raise ValueError("DATABASE_ENGINE не найден в .env файле")
    return create_engine(database_engine)


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
