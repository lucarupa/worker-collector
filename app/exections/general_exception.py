from app.core.Enum.error_code import ErrorCodeEnum


class GeneralException(Exception):
    def __init__(self, message, code: ErrorCodeEnum):
        self.message = message
        self.error_code = code
        super().__init__(message)

    def __str__(self):
        return f"code={self.error_code}, message={self.message}"
