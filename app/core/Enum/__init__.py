from enum import Enum


class ExecutionTypeEnum(Enum):
    API = "api"
    SCRAPPER = "scrapper"


class ReportTypeEnum(Enum):
    ACCOUNT = "ACCOUNT"
    MEMBER = "MEMBER"
    ACCOUNT_MEMBER = "ACCOUNT_MEMBER"


class SaveDataTypeEnum(Enum):
    S3_BUCKET = "S3_BUCKET"
    MONGO = "MONGO"
