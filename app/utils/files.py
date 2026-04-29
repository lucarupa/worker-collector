from pathlib import Path


class UtilsFile:

    @staticmethod
    def find_folder(path: str) -> str:
        local_path = Path(path)
        parts = local_path.parts
        if len(parts) >= 2:
            return parts[-2]
        else:
            return ""
