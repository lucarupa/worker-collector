from abc import ABC
from typing import Generic, TypeVar, List

from app.core.Enum.error_code import ErrorCodeEnum
from app.adapter.interface import StrategyInterface
from app.core.interface.normalization_interface import NormalizationInterface
from app.core.interface.operator_interface import OperatorInterface
from app.core.interface.start_collector_interface import StartCollector
from app.exections.general_exception import GeneralException
from app.utils.logger import AppLogger

T = TypeVar("T")


class StrategyModel(ABC, Generic[T]):
    def __init__(self, data: StrategyInterface):
        self.logger = AppLogger(__name__, "app.log").get_logger()
        self.config: T = data.Config
        self.operator: OperatorInterface = data.operator
        self.normalization: NormalizationInterface = data.normalization

        self.path_list: List[str] | None = None

    def _run_processor(self, data: StartCollector) -> List[str]:
        pass

    def _run_normalization(self):
        pass

    def _run_operator(self):
        pass

    def _add_column_percentage(self):
        pass

    def _select_and_separate(self) -> List[str]:
        pass

    def execute(self, data: StartCollector):
        try:
            self.logger.info("estar collector")
            self.path_list = self._run_processor(data)
            if self.path_list and len(self.path_list) > 0:
                self._run_normalization()
                self._add_column_percentage()
                self._run_operator()
            else:
                raise GeneralException("Not found data", ErrorCodeEnum.NOT_FOUND_DATA)
        except GeneralException as e:
            raise e
