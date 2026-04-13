import os.path
from typing import List

from app.adapter.interface import StrategyInterface
from app.adapter.model import StrategyModel
from app.core.const import FOLDER_SAVE_PATH
from app.core.interface.config_interface import ApiConfigInterface
from app.core.interface.start_collector_interface import StartCollector
from app.exections.general_exception import GeneralException
from app.utils.logger import AppLogger


class ApiImplementations(StrategyModel):
    def __init__(self, data: StrategyInterface):
        super().__init__(data)
        self.config: ApiConfigInterface = data.config
        self.logger = AppLogger("Api Implementations", "app.log").get_logger()

    def _run_processor(self, data: StartCollector) -> List[str]:
        try:
            csv_folder = os.path.join(FOLDER_SAVE_PATH, self.config.s3_path)
            folder_path = os.path.abspath(csv_folder)
            return [folder_path]
        except GeneralException as e:
            raise e
