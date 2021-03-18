import os

from ochs.utils.fs import is_or_mkdir
from ochs.utils.logging import logger


def compile_source(source_dir: str, target_dir: str) -> bool:
    if not validate_directories(source_dir, target_dir):
        return False

    logger().error("Full compilation not yet implemented.")
    return True


def validate_directories(source_dir: str, target_dir: str) -> bool:
    if not os.path.isdir(source_dir):
        logger().error(f"Source directory '{source_dir}' is not valid.")
        return False

    if not is_or_mkdir(target_dir):
        logger().error(f"Target directory '{target_dir}' cannot be created.")
        return False

    return True
