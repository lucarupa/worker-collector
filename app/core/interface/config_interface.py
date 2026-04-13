from pydantic import BaseModel

from app.core.Enum import ReportTypeEnum


class Config(BaseModel):
    id: str
    slug: str
    s3_path: str
    connect_vpn: bool
    vpn_name: str
    percentage: float
    is_active: bool
    affiliation: str
    report: ReportTypeEnum
    create_at: str
    update_at: str


class ScrapperConfigInterface(Config):
    username: str
    password: str
    url_login: str
    url_member: str
    url_account: str


class ApiConfigInterface(Config):
    base: str
    member: str
    account: str
