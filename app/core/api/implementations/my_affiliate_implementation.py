from app.core.Enum import ReportTypeEnum
from app.core.api.interface import StartApiCollector
from app.core.api.model import ApisAffiliationStrategyBase
from app.exections.general_exception import GeneralException
from app.utils.logger import AppLogger


class MyAffiliateImplementation(ApisAffiliationStrategyBase):

    def __init__(self):
        super().__init__()
        self.logger = AppLogger(__name__, "app.log").get_logger()

    def execute_member(self, token: dict, info_collector: StartApiCollector) -> str:
        path_file = ""
        self.logger.info(
            f"Start executing of {info_collector.properties.slug} for dates {info_collector.from_date} - {info_collector.to_date}"
        )
        try:
            url, headers = self.get_credentials(
                token=token,
                info_collector=info_collector,
                report_type=ReportTypeEnum.MEMBER,
            )
            return path_file
        except GeneralException as err:
            raise err

    def execute_account(self, token: dict, info_collector: StartApiCollector) -> str:
        pass
