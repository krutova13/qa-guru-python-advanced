from requests import Response

from test_framework.clients.api_client import ApiClient


class ProductsApiClient(ApiClient):

    def __init__(self, env):
        super().__init__(env)

    def create_product(self, product: dict) -> Response:
        return self.session.post("/products", json=product)
