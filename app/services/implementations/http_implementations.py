from typing import Any

from app.core.interface.http_interface import HttpsTypeEnum
from app.services.model.http import HttpBase


class HttpImplementations(HttpBase):
    _instance = None

    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = super(HttpImplementations, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True

    def get(
        self, base_url: str, headers: dict = None, response_type: HttpsTypeEnum = None
    ) -> Any:
        pass

    def post(
        self,
        base_url: str,
        body=None,
        headers: dict = None,
        response_type: HttpsTypeEnum = None,
    ) -> Any:
        pass
