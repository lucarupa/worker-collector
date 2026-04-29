from enum import Enum


class DateFormatEnum(Enum):
    DATE_STANDARD = "%Y-%m-%d"
    DATE_DAY = "%d/%m/%Y"
    DATE_DAY_BASH = "%d-%m-%Y"
    DATE_SLASH = "%Y/%m/%d"
    DATE_YEAR = "%Y-%d-%m"
    DATE_MONTH = "%m/%d/%Y"
    DATE_MONTH_NAME = "%d %B %Y"
