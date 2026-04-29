from enum import Enum


class ErrorCodeEnum(Enum):
    EXEC_ERROR = "EE_001"
    EXEC_NOT_STRATEGY = "EE_002"
    INTERNAL_ERROR_SITE = "IES_001"
    NOT_FOUND_DATA = "NFD_001"
    UNKNOWN_ERROR = "UE_001"
