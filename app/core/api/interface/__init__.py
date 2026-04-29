from datetime import datetime

from pydantic import BaseModel, validator

from app.core.interface.config_interface import ApiConfigInterface


class StartApiCollector(BaseModel):
    properties: ApiConfigInterface
    date_column_name: str
    format_date: str
    folder_path: str
    from_date: str
    to_date: str
    delete_rows: int

    @validator("from_date", "to_date")
    def date_columns_validator(cls, v):
        datetime.strptime(v, "%Y-%m-%d")

    @validator("delete_rows")
    def delete_rows_validator(cls, v):
        if v < 0:
            raise ValueError("delete_rows cannot be negative")
        return v

    class Config:
        arbitrary_types_allowed = True
