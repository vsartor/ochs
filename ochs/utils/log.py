import logging
import re
import sys
from functools import lru_cache
from typing import Optional

from ochs.utils.term import bold


def setup_logger(debug: bool) -> None:
    """
    Sets the configuration for the logging parameter.
    """

    logging_level = logging.DEBUG if debug else logging.INFO

    formatter = logging.Formatter("[\u001b[1m%(levelname)-7s\u001b[0m] - %(message)s")

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(formatter)

    logger().setLevel(logging_level)
    logger().addHandler(console_handler)


@lru_cache(maxsize=None)
def logger() -> logging.Logger:
    return logging.getLogger("ochs")


def info(message: str, highlight_delim: Optional[str] = "'") -> None:
    logger().info(highlight(message, highlight_delim))


def warning(message: str, highlight_delim: Optional[str] = "'") -> None:
    logger().warning(highlight(message, highlight_delim))


def error(message: str, highlight_delim: Optional[str] = "'") -> None:
    logger().error(highlight(message, highlight_delim))


def highlight(message: str, delim: str) -> str:
    matches = set(re.findall(f"{delim}.+{delim}", message))
    for match in matches:
        message = message.replace(match, bold(match))
    return message
