import os
import shutil

from ochs.builder.pages import build_pages
from ochs.builder.posts import build_posts
from ochs.utils.fs import is_or_mkdir
from ochs.utils.logging import logger
from ochs.utils.term import bold


def compile_source(source_dir: str, target_dir: str) -> bool:
    if not os.path.isdir(source_dir):
        logger().error(f"Source directory '{source_dir}' is not valid.")
        return False

    if not prepare_target_dir(source_dir, target_dir):
        return False

    build_pages(source_dir, target_dir)
    build_posts(source_dir, target_dir)

    logger().error("Full compilation not yet implemented.")
    return True


def prepare_target_dir(source_dir: str, target_dir: str) -> bool:
    if os.path.isdir(target_dir):
        logger().warning(f"Deleting old '{bold(target_dir)}'.")
        shutil.rmtree(target_dir)

    logger().info(f"Creating target '{bold(target_dir)}'.")
    shutil.copytree(f"{source_dir}/static", target_dir)

    if not is_or_mkdir(f"{target_dir}/posts"):
        logger().error("Posts directory cannot be created.")
        return False

    return True
