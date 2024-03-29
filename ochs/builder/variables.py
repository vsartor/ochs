import re
from functools import lru_cache

from ochs.flags import flag
from ochs.utils import log
from ochs.utils.fs import read_yaml

_AT_MASK = "__ochs_at_mask_"


@lru_cache(maxsize=None)
def load_global_variables(source_dir: str) -> dict[str, str]:
    global_variables = read_yaml(f"{source_dir}/variables.yaml")
    for key, value in global_variables.items():
        if isinstance(value, dict):
            if flag.prod and "prod" in value:
                global_variables[key] = value["prod"]
            else:
                global_variables[key] = value["default"]
    return global_variables


def apply_global_variables(content: str, source_dir: str) -> str:
    global_variables = load_global_variables(source_dir)
    return apply_variables(content, global_variables)


def apply_variables(content: str, variables: dict[str, str]) -> str:
    log.info(f"Applying variables: {variables}")
    content = content.replace("@@{", _AT_MASK)
    for name, value in variables.items():
        content = content.replace(f"@{{{name}}}", value)
    return content.replace(_AT_MASK, "@{")


def check_unfilled_variables(content: str) -> None:
    regexp_rule = r"@\{(.*?)\}"
    matches = re.finditer(regexp_rule, content)
    for match in matches:
        log.error(f"Found non-expanded variable '{match.group(1)}'.")
