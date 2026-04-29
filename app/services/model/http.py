from abc import ABC, abstractmethod
from typing import Any

from app.core.interface.http_interface import HttpsTypeEnum


class HttpBase(ABC):

    @abstractmethod
    def get(
        self, base_url: str, headers: dict = None, response_type: HttpsTypeEnum = None
    ) -> Any:
        pass

    @abstractmethod
    def post(
        self,
        base_url: str,
        body=None,
        headers: dict = None,
        response_type: HttpsTypeEnum = None,
    ) -> Any:
        pass
