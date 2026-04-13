from typing import List

from pydantic import BaseModel

from app.core.Enum import ReportTypeEnum


class RenameColumnsInterface(BaseModel):
    column_name: str
    new_column_name: str
    column_is_number: bool


class NormalizationInterface(BaseModel):
    id: str
    slug: str
    report: ReportTypeEnum
    date_column_name: str
    date_columns: List[str]
    format_date: str
    delete_rows: int
    rename_member_columns: List[RenameColumnsInterface]
    group_member_columns: List[str]
    select_member_columns: List[str]
    rename_account_columns: List[RenameColumnsInterface]
    group_account_columns: List[str]
    select_account_columns: List[str]
    create_at: str
    update_at: str
