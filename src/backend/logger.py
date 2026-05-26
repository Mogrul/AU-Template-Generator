import logging
import sys
import re

class Formatter(logging.Formatter):
    TIME = "\x1b[1;90m"
    LEVEL = "\x1b[34m"
    NAME = "\x1b[35m"
    BOLD_WHITE = "\x1b[1;37m"
    RESET = "\x1b[0m"

    def format(self, record):
        time = f"{self.TIME}{self.formatTime(record, '%Y-%m-%d %H:%M:%S')}{self.RESET}"
        level = f"{self.LEVEL}{record.levelname:<8}{self.RESET}"
        name = f"{self.NAME}{record.name}{self.RESET}"

        message = record.getMessage()

        message = re.sub(
            r"\*(.*?)\*",
            lambda m: f"{self.BOLD_WHITE}{m.group(1)}{self.RESET}",
            message
        )

        return f"{time} {level} {name} {message}"

class FileFormatter(logging.Formatter):
    def format(self, record):
        time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        return f"{time} {record.levelname:<8} {record.name} {record.getMessage()}"

def load_logger_config() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console (colored)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(Formatter())

    # File (plain)
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setFormatter(FileFormatter())

    logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)