import logging

from colorama import Fore, Style, init


def colored_formatter():
    colors = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            level_color = colors.get(record.levelno, Fore.WHITE)
            formatter = logging.Formatter(
                f"{level_color}%(asctime)s - %(name)s - %(levelname)s - %(message)s{Style.RESET_ALL}"
            )
            return formatter.format(record)

    return ColoredFormatter()


class AppLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, name, log_file, level=logging.INFO):
        if not self._initialized:
            init()
            self.logger = logging.getLogger(name)
            self.logger.setLevel(level)

            if not self.logger.hasHandlers():
                file_formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
                self.formatter = colored_formatter()

                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(level)
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)
                console_handler.setFormatter(self.formatter)
                self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
