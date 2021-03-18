import logging
import sys
from functools import lru_cache


def setup_logger(debug: bool) -> None:
    """
    Sets the configuration for the logging parameter.
    """

    logging_level = logging.DEBUG if debug else logging.INFO

    formatter = logging.Formatter(
        "[%(filename)12s:%(lineno)4d] \u001b[1m%(levelname)-8s\u001b[0m - %(message)s"
    )

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(formatter)

    logger().setLevel(logging_level)
    logger().addHandler(console_handler)


@lru_cache(maxsize=None)
def logger() -> logging.Logger:
    """Returns a Logger object."""

    return logging.getLogger("ochs")
