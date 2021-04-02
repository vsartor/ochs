"""Utility functions for dealing with the user's filesystem."""


import os

import markdown
import yaml


def read(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def read_md(path: str) -> str:
    return markdown.markdown(read(path), extensions=["extra", "mdx_math"])


def read_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def write(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def is_or_mkdir(path: str) -> bool:
    """
    Checks that the given path is a directory. In case it does not exist, it creates the
    directory. It returns true if the directory exists at the end of the function, and false
    in case the directory could not be created.
    """

    if os.path.isdir(path):
        return True

    if not os.path.exists(path):
        os.mkdir(path)
        # To preventing returning True in case os.mkdir fails silently, let's check that
        # the created directory actually was created.
        return os.path.isdir(path)

    # If we got here, the given path exists and is not a directory.
    return False
