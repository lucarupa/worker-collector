from typing import Union

from injector import Injector

from app.adapter.implementations.scrapper_implementations import ScrapperImplementations
from app.core.Enum import ExecutionTypeEnum
from app.core.Enum.error_code import ErrorCodeEnum
from app.adapter.implementations.api_implementations import ApiImplementations
from app.adapter.interface import StrategyInterface
from app.core.const import (
    create_api_config,
    create_scrapper_config,
    create_normalization,
    create_operator,
)
from app.core.interface.config_interface import (
    ApiConfigInterface,
    ScrapperConfigInterface,
)
from app.core.interface.start_collector_interface import StartCollector
from app.exections.general_exception import GeneralException
from app.utils.logger import AppLogger


class CollectorAdapter:
    def __init__(self, injector: Injector):
        self.logger = AppLogger(__name__, "app.log").get_logger()
        self.is_executing = False
        self.execution_type = ExecutionTypeEnum.API
        self.strategy: Union[None, ApiImplementations, ScrapperImplementations] = None
        self._init_repository()

    def _init_repository(self):
        pass

    def _init_strategy(self):
        try:
            if self.execution_type == ExecutionTypeEnum.API:
                config: ApiConfigInterface = create_api_config()
            else:
                config: ScrapperConfigInterface = create_scrapper_config()
            strategy = StrategyInterface(
                config=config,
                normalization=create_normalization(),
                operator=create_operator(),
            )
            if self.execution_type == ExecutionTypeEnum.API:
                self.strategy = ApiImplementations(strategy)
            else:
                self.strategy = ScrapperImplementations(strategy)
        except Exception as e:
            message = f"Configuration execution error: {str(e)}"
            self.logger.error(message)
            raise GeneralException(message, ErrorCodeEnum.INTERNAL_ERROR_SITE)

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
            self.execution_type = info.executeBy
            self._init_strategy()
            if self.strategy is not None:
                self.strategy.execute(info)
        except GeneralException as e:
            raise e
        finally:
            self.is_executing = False
            self.strategy = None
            self.strategy = None
