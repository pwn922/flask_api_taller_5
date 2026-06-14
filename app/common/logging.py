import logging
import sys

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

COLORS = {
    "TRACE": "\033[38;5;244m",
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[41;97m",
}

LEVEL_COLORS = {
    "TRACE": "\033[38;5;244m",
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[41;97m",
}

SOURCE_COLORS = {
    "uvicorn": "\033[35m",
    "pymongo": "\033[38;5;240m",
    "motor": "\033[38;5;240m",
}


def _source_color(name: str) -> str:
    for prefix, color in SOURCE_COLORS.items():
        if name.startswith(prefix):
            return color
    return "\033[34m"


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        level_color = LEVEL_COLORS.get(record.levelname, RESET)
        source_color = _source_color(record.name)

        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        levelname = f"{level_color}{record.levelname:<7}{RESET}"
        sourcename = f"{source_color}{record.name:<25}{RESET}"
        message = record.getMessage()

        return f"{DIM}{timestamp}{RESET} | {levelname} | {sourcename} | {message}"


def setup_logging(env: str = "development") -> None:
    level = logging.DEBUG if env == "development" else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("arangoasync").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
