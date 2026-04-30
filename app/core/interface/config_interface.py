from pydantic import BaseModel

from app.core.Enum import ReportTypeEnum
from app.core.interface.normalization_interface import RenameColumnsInterface


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


class AuthConfigInterface(BaseModel):
    url: str
    client_id: str
    client_secret: str
    scope: str
    grant_type: str


class BaseConfigInterface(BaseModel):
    url: str
    query: str
    header: dict[str, str]


class GroupConfigInterface(BaseModel):
    names: list[str]
    select: list[str]
    renames: list[RenameColumnsInterface]


class ConfigReportInterface(BaseModel):
    endpoint: str
    query: str
    group: list[GroupConfigInterface]


class ApiConfigInterface(Config):
    auth: AuthConfigInterface
    base: BaseConfigInterface
    member: ConfigReportInterface
    account: ConfigReportInterface
