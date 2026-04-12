from app.core.Enum import ExecutionTypeEnum
from app.core.Enum.error_code import ErrorCodeEnum
from app.core.interface.start_collector import StartCollector
from app.exections.general_exception import GeneralException
from app.utils.logger import AppLogger


class CollectorAdapter:
    def __init__(self):
        self.logger = AppLogger(__name__, "app.log").get_logger()
        self.is_executing = False
        self.execution_type = ExecutionTypeEnum.API
        self.strategy = None
        self._init_repository()

    def _init_repository(self):
        pass

    def _init_strategy(self):
        pass

    def execute(self, info: StartCollector):
        if self.is_executing:
            self.logger.error("Execution already in progress")
            raise GeneralException(
                "A scrapper operation is already in progress. Please wait until it finishes.",
                ErrorCodeEnum.EXEC_ERROR,
            )
        if not info.executeBy:
            message = "not strategy defined"
            self.logger.error(message)
            raise GeneralException(message, ErrorCodeEnum.EXEC_NOT_STRATEGY)
        try:
            self.is_executing = True
        except GeneralException as e:
            raise e
        finally:
            self.is_executing = False
            self.strategy = None
