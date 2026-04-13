from typing import Optional, Dict

from injector import inject
from jinja2.nodes import List

from app.core.Enum import ReportTypeEnum
from app.core.interface.config_interface import ApiConfigInterface
from app.services.model.database import Database


class ApiConfigRepository:

    @inject
    def __init__(self, db: Database):
        self.db = db
        self._initialized = True

    def get_config(
        self, slug: str, report: ReportTypeEnum
    ) -> Optional[ApiConfigInterface]:
        query = {
            "slug": slug,
            "report": report.value,
        }
        result: List[Dict] = self.db.query("api_config", query)
        if len(result) == 0:
            return None

        return ApiConfigInterface(**result[0])

    def disconnect(self):
        self.db.disconnect()
