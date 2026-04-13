from typing import Optional, Dict

from injector import inject
from jinja2.nodes import List

from app.core.Enum import ReportTypeEnum
from app.core.interface.config_interface import ScrapperConfigInterface
from app.services.model.database import Database


class ScrapperConfigRepository:

    @inject
    def __init__(self, db: Database):
        self.db = db
        self._initialized = True

    def get_config(
        self, slug: str, report: ReportTypeEnum
    ) -> Optional[ScrapperConfigInterface]:
        query = {
            "slug": slug,
            "report": report.value,
        }
        result: List[Dict] = self.db.query("scrapper_config", query)
        if len(result) == 0:
            return None

        return ScrapperConfigInterface(**result[0])

    def disconnect(self):
        self.db.disconnect()
