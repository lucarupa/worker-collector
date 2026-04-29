from datetime import datetime


class UtilsDates:

    @staticmethod
    def date_format(date: str, input_format: str, output_format: str) -> str:
        return datetime.strptime(date, input_format).strftime(output_format)
