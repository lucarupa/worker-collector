from pydantic import BaseModel

from app.core.Enum import ExecutionTypeEnum, ReportTypeEnum, SaveDataTypeEnum


class StartCollector(BaseModel):
    id: str
    fromDate: str
    toDate: str
    slug: str
    executeBy: ExecutionTypeEnum
    reportType: ReportTypeEnum
    saveBy: SaveDataTypeEnum
