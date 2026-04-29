import os
import shutil
from datetime import datetime
from pathlib import Path

from app.core.Enum import ReportTypeEnum
from app.core.Enum.date_format import DateFormatEnum
from app.core.Enum.error_code import ErrorCodeEnum
from app.exections.general_exception import GeneralException


class UtilsFile:

    @staticmethod
    def check_if_dir_exists_or_create(path: str):
        exist_path = os.path.exists(path)
        if not exist_path:
            os.mkdir(path)

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

    def rename_file(self, filename, folder_path, last_file) -> bool:
        try:
            path = self.find_folder_download()
            new_file = os.path.join(path, filename)
            os.rename(last_file, new_file)
            self.check_if_dir_exists_or_create(folder_path)
            shutil.copy2(new_file, os.path.join(folder_path, filename))
            os.remove(new_file)
            return True
        except GeneralException as error:
            raise error
        except Exception as error:
            message = f"Error in rename_files: {repr(error)}"
            raise GeneralException(message, ErrorCodeEnum.UNKNOWN_ERROR)

    def move_the_file_from_downloads_folder_to_the_project_folder(
        self, folder_path: str, report_type: ReportTypeEnum, file_path: str
    ) -> str:
        try:
            today = datetime.today().strftime(DateFormatEnum.DATE_STANDARD.value)
            file_name = f"{report_type.value}_{today}_report.csv"
            original_file = os.path.join(folder_path, file_name)
            rename = self.rename_file(
                filename=file_name, folder_path=folder_path, last_file=file_path
            )
            if rename:
                return original_file
            else:
                raise GeneralException(
                    "Not found file", ErrorCodeEnum.INTERNAL_ERROR_SITE
                )
        except GeneralException as error:
            raise error
        except Exception as error:
            message = f"Error in rename_file: {repr(error)}"
            raise GeneralException(message, ErrorCodeEnum.UNKNOWN_ERROR)
