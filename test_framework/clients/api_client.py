from requests import Response

from test_framework.config import Server
from test_framework.session.base_session import BaseSession


class ApiClient:
    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).service)

    def request(
            self,
            method: str,
            url: str,
            params: dict = None,
            body: dict = None,
            headers: dict = None,
            **kwargs
    ) -> Response:
        return self.session.request(
            method=method,
            url=url,
            params=params,
            json=body,
            headers=headers,
            **kwargs
        )
