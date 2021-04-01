from functools import lru_cache
from typing import NamedTuple

from ochs.builder.page import Page
from ochs.builder.templates import get_template
from ochs.builder.variables import apply_global_variables, apply_variables
from ochs.utils.fs import read_yaml, write
from ochs.utils import log


class PageSpec(NamedTuple):
    template: str
    url: str
    variables: dict[str, str]


@lru_cache(maxsize=None)
def load_specs(source_dir: str) -> list[PageSpec]:
    return [
        PageSpec(
            template=raw_spec["template"],
            url=raw_spec["url"],
            variables=raw_spec["variables"],
        )
        for raw_spec in read_yaml(f"{source_dir}/pages.yaml")
    ]


def load_page(source_dir: str, spec: PageSpec) -> Page:
    content = get_template(source_dir, spec.template)
    content = apply_global_variables(content, source_dir)
    content = apply_variables(content, spec.variables)
    return Page(url=spec.url, content=content)


def build_pages(source_dir: str, target_dir: str) -> None:
    specs = load_specs(source_dir)
    pages = [load_page(source_dir, spec) for spec in specs]

    for page in pages:
        page.write(target_dir)
