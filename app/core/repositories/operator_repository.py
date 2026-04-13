from typing import Optional, Dict

from injector import inject
from jinja2.nodes import List

from app.core.Enum import ReportTypeEnum
from app.core.interface.normalization_interface import NormalizationInterface
from app.core.interface.operator_interface import OperatorInterface
from app.services.model.database import Database


class OperatorRepository:

    @inject
    def __init__(self, db: Database):
        self.db = db
        self._initialized = True

    def get_config(
        self, slug: str, report: ReportTypeEnum
    ) -> Optional[OperatorInterface]:
        query = {
            "slug": slug,
            "report": report.value,
        }
        result: List[Dict] = self.db.query("operators", query)
        if len(result) == 0:
            return None

        return OperatorInterface(**result[0])

    def disconnect(self):
        self.db.disconnect()
