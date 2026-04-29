import gc
from abc import ABC, abstractmethod
from unittest import result

from app.core.Enum import ReportTypeEnum
from app.core.api.interface import StartApiCollector
from app.core.interface.config_interface import ApiConfigInterface
from app.core.interface.http_interface import HttpsTypeEnum
from app.exections.general_exception import GeneralException
from app.services.implementations.http_implementations import HttpImplementations
from app.utils.dates import UtilsDates
from app.utils.files import UtilsFile
from app.utils.logger import AppLogger


class ApisAffiliationStrategyBase(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ApisAffiliationStrategyBase).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.http_service = HttpImplementations()
            self.utils_file = UtilsFile()
            self.utils_date = UtilsDates()
            self.logger = AppLogger(__name__, "app.log").get_logger()
            self._initialized = True

    def get_token(self, info_collector: StartApiCollector) -> dict:
        data = {
            "scope": info_collector.properties.auth.scope,
            "client_id": info_collector.properties.auth.client_id,
            "grant_type": info_collector.properties.auth.grant_type,
            "client_secret": info_collector.properties.auth.client_secret,
        }
        result = self.http_service.post(
            base_url=info_collector.properties.auth.url,
            body=data,
            response_type=HttpsTypeEnum.DATA,
        )
        return dict(result)

    @staticmethod
    def get_headers(token: dict) -> dict:
        if "token_type" in token and "access_token" in token:
            headers = {
                "Authorization": f"{token['token_type']} {token['access_token']}",
            }
        else:
            headers = {}
        return headers

    def get_credentials(
        self,
        info_collector: ApiConfigInterface,
        report_type: ReportTypeEnum,
        token: dict,
        start_date: str,
        end_date: str,
    ) -> tuple[str, dict]:
        url_base = info_collector.base.url
        if report_type == ReportTypeEnum.MEMBER:
            endpoint = (
                f"{info_collector.member.endpoint}&{info_collector.member.query}&"
            )
        else:
            endpoint = (
                f"{info_collector.account.endpoint}&{info_collector.account.query}&"
            )
        headers = self.get_headers(token)
        url = f"{url_base}/{endpoint}d1={start_date}&d2={end_date}&{info_collector.base.query}"
        return url, headers

    def download_report(
        self,
        url: str,
        slug: str,
        headers: dict = None,
        report_type: HttpsTypeEnum = None,
    ) -> tuple[bool, str]:
        try:
            result_report = self.http_service.get(
                base_url=url, headers=headers, response_type=report_type
            )
            file_name_origin = f"{slug}_report.csv"
            folder_download = self.utils_file.find_folder_download()
            file_name = f"{folder_download}/{file_name_origin}"
            if result_report.content:
                with open(file_name, "wb") as file:
                    file.write(result_report.content)
                    return True, file_name
            return False, file_name
        except GeneralException as error:
            raise error

    @abstractmethod
    def execute_member(
        self,
        token: dict,
        info_collector: StartApiCollector,
    ) -> str:
        pass

    @abstractmethod
    def execute_account(
        self,
        token: dict,
        info_collector: StartApiCollector,
    ) -> str:
        pass

    def execute(self, info_collector: StartApiCollector) -> list[str]:
        try:
            path_list_file: list[str] = []
            token = self.get_token(info_collector)
            if info_collector.properties.report == ReportTypeEnum.MEMBER:
                file = self.execute_member(token=token, info_collector=info_collector)
                if file and file != "":
                    path_list_file.append(file)
            elif info_collector.properties.report == ReportTypeEnum.ACCOUNT:
                file = self.execute_account(token=token, info_collector=info_collector)
                if file and file != "":
                    path_list_file.append(file)
            else:
                member = self.execute_member(token=token, info_collector=info_collector)
                if member and member != "":
                    path_list_file.append(member)
                account = self.execute_account(
                    token=token, info_collector=info_collector
                )
                if account and account != "":
                    path_list_file.append(account)
            return path_list_file
        except GeneralException as error:
            raise error
        finally:
            gc.collect()
