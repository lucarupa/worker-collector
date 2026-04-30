from app.core.Enum import ReportTypeEnum
from app.core.Enum.error_code import ErrorCodeEnum
from app.core.api.interface import StartApiCollector
from app.core.api.model import ApisAffiliationStrategyBase
from app.core.interface.http_interface import HttpsTypeEnum
from app.exections.general_exception import GeneralException
from app.utils.logger import AppLogger


class MyAffiliateImplementation(ApisAffiliationStrategyBase):

    def __init__(self):
        super().__init__()
        self.logger = AppLogger(__name__, "app.log").get_logger()

    def execute_member(self, token: dict, info_collector: StartApiCollector) -> str:
        self.logger.info(
            f"Starting execution of {info_collector.properties.slug} for dates {info_collector.from_date} - {info_collector.to_date} - Member"
        )
        try:
            url, headers = self.get_credentials(
                token=token,
                info_collector=info_collector.properties,
                report_type=ReportTypeEnum.MEMBER,
                start_date=str(info_collector.from_date),
                end_date=str(info_collector.to_date),
            )
            download, file = self.download_report(
                url=url,
                headers=headers,
                report_type=HttpsTypeEnum.DOCUMENT,
                slug=info_collector.properties.slug,
            )
            if download:
                self.logger.info("Move the downloaded file to the project folder")
                path_file = self.utils_file.move_the_file_from_downloads_folder_to_the_project_folder(
                    folder_path=info_collector.folder_path,
                    report_type=ReportTypeEnum.MEMBER,
                    file_path=file,
                )
                return path_file
            else:
                raise GeneralException("Not found data", ErrorCodeEnum.NOT_FOUND_DATA)
        except GeneralException as err:
            raise err

    def execute_account(self, token: dict, info_collector: StartApiCollector) -> str:
        self.logger.info(
            f"Starting execution of {info_collector.properties.slug} for dates {info_collector.from_date} - {info_collector.to_date} - Account"
        )
        path_file = ""
        return path_file
