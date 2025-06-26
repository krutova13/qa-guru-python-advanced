from requests import Response

from test_framework.clients.api_client import ApiClient


class ProductsApiClient(ApiClient):

    def __init__(self, env):
        super().__init__(env)

    def create_product(self, product: dict) -> Response:
        return self.session.post("/products", json=product)

    def get_all_products(self, params=None) -> Response:
        return self.session.get("/products", params=params)

    def get_product_by_id(self, product_id: int) -> Response:
        return self.session.get(f"/products/{product_id}")

    def delete_product(self, product_id: int) -> Response:
        return self.session.delete(f"/products/{product_id}")
