import re
from functools import lru_cache

from ochs.utils.fs import read
from ochs.utils.logging import logger
from ochs.utils.term import bold


@lru_cache(maxsize=None)
def get_template(source_dir: str, template_name: str) -> str:
    logger().info(f"Loading template '{bold(template_name)}' from disk.")
    content = read(f"{source_dir}/templates/{template_name}.html")

    sub_templates = {name[2:][:-1] for name in re.findall(r"\$\{[a-zA-Z-]+\}", content)}
    for template_name in sub_templates:
        content = content.replace(f"${{{template_name}}}", get_template(source_dir, template_name))

    return content
