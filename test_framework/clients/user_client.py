from requests import Response

from app.models.models import UserUpdate
from test_framework.clients.api_client import ApiClient


class UsersApiClient(ApiClient):

    def __init__(self, env):
        super().__init__(env)

    def get_all_users(self) -> Response:
        return self.session.get("/users")

    def get_user_by_id(self, user_id: int) -> Response:
        return self.session.get(f"/users/{user_id}")

    def update_user(self, user_id: int, user_update: UserUpdate) -> Response:
        return self.session.patch(f"/users/{user_id}", json=user_update.model_dump())

    def create_user(self, user: dict) -> Response:
        return self.session.post("/users", json=user)

    def delete_user(self, user_id: int) -> Response:
        return self.session.delete(f"/users/{user_id}")

    def get_user_products(self, user_id: int) -> Response:
        return self.session.get(f"/users/{user_id}/products")

    def get_user_product(self, user_id: int, product_id: int) -> Response:
        return self.session.get(f"/users/{user_id}/products/{product_id}")
