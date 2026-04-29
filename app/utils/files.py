import os
from pathlib import Path

from app.core.Enum.error_code import ErrorCodeEnum
from app.exections.general_exception import GeneralException


class UtilsFile:

    @staticmethod
    def find_folder(path: str) -> str:
        local_path = Path(path)
        parts = local_path.parts
        if len(parts) >= 2:
            return parts[-2]
        else:
            return ""

    @staticmethod
    def find_folder_download() -> str:
        try:
            home = os.path.expanduser("~")
            path = os.path.join(home, "Downloads")
            return path
        except Exception as e:
            raise GeneralException(e, ErrorCodeEnum.UNKNOWN_ERROR)
