from typing import List

from pydantic import BaseModel

from app.core.Enum import ReportTypeEnum


class ExpressionInterface(BaseModel):
    name: str
    operation: str
    search_the_information: bool
    value_within_information: bool
    value_information: str


class OperatorInterface(BaseModel):
    id: str
    slug: str
    report: ReportTypeEnum
    expression_member: List[ExpressionInterface]
    expression_account: List[ExpressionInterface]
