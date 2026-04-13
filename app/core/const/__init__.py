from typing import List

from app.core.Enum import ReportTypeEnum
from app.core.interface.config_interface import (
    ScrapperConfigInterface,
    ApiConfigInterface,
)
from app.core.interface.normalization_interface import (
    RenameColumnsInterface,
    NormalizationInterface,
)
from app.core.interface.operator_interface import ExpressionInterface, OperatorInterface

FOLDER_SAVE_PATH = "csv"
FOLDER_NORMALIZE_SAVE_PATH = "normalize"


def create_api_config() -> ApiConfigInterface:
    return ApiConfigInterface(
        is_active=True,
        s3_path="",
        vpn_name="",
        create_at="",
        update_at="",
        account="",
        affiliation="",
        percentage=0.2,
        connect_vpn=False,
        id="",
        base="",
        slug="",
        member="",
        report=ReportTypeEnum.ACCOUNT_MEMBER,
    )


def create_scrapper_config() -> ScrapperConfigInterface:
    return ScrapperConfigInterface(
        is_active=True,
        s3_path="",
        vpn_name="",
        create_at="",
        update_at="",
        connect_vpn=True,
        report=ReportTypeEnum.ACCOUNT_MEMBER,
        slug="",
        percentage=0.6,
        affiliation="",
        id="",
        url_login="",
        password="",
        username="",
        url_member="",
        url_account="",
    )


def create_rename_columns() -> List[RenameColumnsInterface]:
    colum = RenameColumnsInterface(
        column_name="", new_column_name="", column_is_number=True
    )
    return [colum]


def create_normalization() -> NormalizationInterface:
    return NormalizationInterface(
        create_at="",
        update_at="",
        report=ReportTypeEnum.ACCOUNT_MEMBER,
        slug="",
        id="",
        group_member_columns=[""],
        date_columns=[""],
        date_column_name="",
        group_account_columns=[""],
        rename_member_columns=create_rename_columns(),
        rename_account_columns=create_rename_columns(),
        select_member_columns=[],
        select_account_columns=[],
        delete_rows=2,
        format_date="",
    )


def create_expression() -> ExpressionInterface:
    return ExpressionInterface(
        name="",
        operation="",
        value_information="",
        value_within_information=False,
        search_the_information=False,
    )


def create_operator() -> OperatorInterface:
    return OperatorInterface(
        id="",
        slug="",
        report=ReportTypeEnum.ACCOUNT_MEMBER,
        expression_member=[create_expression()],
        expression_account=[create_expression()],
    )
