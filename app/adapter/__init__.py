from typing import Union

from injector import Injector

from app.adapter.implementations.scrapper_implementations import ScrapperImplementations
from app.core.Enum import ExecutionTypeEnum
from app.core.Enum.error_code import ErrorCodeEnum
from app.adapter.implementations.api_implementations import ApiImplementations
from app.adapter.interface import StrategyInterface
from app.core.interface.config_interface import (
    ApiConfigInterface,
    ScrapperConfigInterface,
)
from app.core.interface.normalization_interface import NormalizationInterface
from app.core.interface.operator_interface import OperatorInterface
from app.core.interface.start_collector_interface import StartCollector
from app.core.repositories.api_config_repository import ApiConfigRepository
from app.core.repositories.normalization_repository import NormalizationRepository
from app.core.repositories.operator_repository import OperatorRepository
from app.core.repositories.scrapper_config_repository import ScrapperConfigRepository
from app.exections.general_exception import GeneralException
from app.utils.logger import AppLogger


class CollectorAdapter:
    def __init__(self, injector: Injector):
        self.logger = AppLogger(__name__, "app.log").get_logger()
        self.is_executing = False
        self.execution_type = ExecutionTypeEnum.API
        self.strategy: Union[None, ApiImplementations, ScrapperImplementations] = None
        self._init_repository(injector)

    def _init_repository(self, injector: Injector):
        self.api_config_repository = injector.get(ApiConfigRepository)
        self.scrapper_config_repository = injector.get(ScrapperConfigRepository)
        self.normalization_repository = injector.get(NormalizationRepository)
        self.operator_repository = injector.get(OperatorRepository)

    def _init_strategy(self, info: StartCollector):
        try:
            if self.execution_type == ExecutionTypeEnum.API:
                config: ApiConfigInterface | None = (
                    self.api_config_repository.get_config(
                        report=info.reportType, slug=info.slug
                    )
                )
            else:
                config: ScrapperConfigInterface | None = (
                    self.scrapper_config_repository.get_config(
                        slug=info.slug, report=info.reportType
                    )
                )
            if config is None:
                raise GeneralException("No config found", ErrorCodeEnum.NOT_FOUND_DATA)
            normalization: NormalizationInterface | None = (
                self.normalization_repository.get_config(
                    report=info.reportType, slug=info.slug
                )
            )
            operator: OperatorInterface | None = self.operator_repository.get_config(
                report=info.reportType, slug=info.slug
            )
            if normalization is None or operator is None:
                raise GeneralException("No config found", ErrorCodeEnum.NOT_FOUND_DATA)
            strategy = StrategyInterface(
                config=config,
                normalization=normalization,
                operator=operator,
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
            self._init_strategy(info)
            if self.strategy is not None:
                self.strategy.execute(info)
        except GeneralException as e:
            raise e
        finally:
            self.is_executing = False
            self.strategy = None
            self.strategy = None
