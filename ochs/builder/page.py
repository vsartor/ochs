from typing import NamedTuple

from ochs.utils import log
from ochs.utils.fs import write


class Page(NamedTuple):
    url: str
    content: str

    def write(self, target_dir: str) -> None:
        log.info(f"Writing '{self.url}'.")
        write(f"{target_dir}/{self.url}", self.content)
