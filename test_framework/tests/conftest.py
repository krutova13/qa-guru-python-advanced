import os

import dotenv as dotenv

from test_framework.clients.api_client import ApiClient
from test_framework.clients.product_client import ProductsApiClient

dotenv.load_dotenv()

import pytest
from sqlmodel import Session, create_engine

from app.models.models import User, Product, UserCreate, ProductCreate
from test_framework.clients.user_client import UsersApiClient
from test_framework.config import Server
from test_framework.session.base_session import BaseSession


@pytest.fixture(scope="session")
def envs():
    if not os.getenv("APP_URL"):
        raise ValueError(f"APP_URL не найден в .env файле")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='function')
def api_client(env):
    with BaseSession(base_url=Server(env).service) as session:
        yield session
    session.close()


@pytest.fixture(scope="function", autouse=True)
def cleanup_database(env):
    yield
    engine = get_test_engine()
    with Session(engine) as session:
        session.query(Product).delete()
        session.query(User).delete()
        session.commit()


@pytest.fixture
def create_user(env: str, valid_user: UserCreate) -> User:
    response = UsersApiClient(env).create_user(valid_user.model_dump())
    return User(**response.json())


@pytest.fixture
def create_product(env: str, valid_product: Product, create_user: User) -> Product:
    product_data = valid_product.copy()
    product_data.user_id = create_user.id
    response = ProductsApiClient(env).create_product(product_data.model_dump())
    return Product(**response.json())


@pytest.fixture
def create_users(env: str, valid_user: UserCreate):
    _delete_items(env, "/users")

    def _create(count):
        for _ in range(count):
            user_data: UserCreate = valid_user.copy()
            UsersApiClient(env).create_user(user_data.model_dump())

    return _create


@pytest.fixture
def create_products(env: str, valid_product: ProductCreate, create_user: User):
    _delete_items(env, "/products")

    def _create(count):
        for _ in range(count):
            product_data = valid_product.copy()
            product_data.user_id = create_user.id
            ProductsApiClient(env).create_product(product_data.model_dump())

    return _create


@pytest.fixture
def valid_user() -> UserCreate:
    return UserCreate(
        name="Test",
        surname="Testov",
        birth_date="01.10.1995",
        products=[]
    )


@pytest.fixture
def invalid_user() -> dict:
    return {
        "name": "Test",
        "surname": "Testov",
        "birth_date": "invalid-date",
        "products": []
    }


@pytest.fixture
def valid_product() -> ProductCreate:
    return ProductCreate(
        title="Test Product",
        description="Test Description",
        price=100.0,
        user_id=None
    )


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


def get_test_engine():
    database_engine = os.getenv("DATABASE_ENGINE")
    if not database_engine:
        raise ValueError("DATABASE_ENGINE не найден в .env файле")
    return create_engine(database_engine)


def get_all_items(env: str, endpoint: str) -> list:
    all_items = []
    page = 1
    while True:
        response = ApiClient(env).request(method="GET", url=endpoint, params={"page": page, "size": 100})
        data = response.json()
        all_items.extend(data["items"])

        if page >= data["pages"]:
            break
        page += 1
    return all_items


def _delete_items(env: str, endpoint: str):
    response = ApiClient(env).request(method="GET", url=endpoint)
    items = response.json()["items"]
    if items:
        for item in items:
            ApiClient(env).request(method="DELETE", url=f"{endpoint}/{item['id']}")
