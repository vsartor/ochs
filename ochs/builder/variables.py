from functools import lru_cache

from ochs.utils.fs import read_yaml


@lru_cache(maxsize=None)
def load_global_variables(source_dir: str) -> dict[str, str]:
    return read_yaml(f"{source_dir}/variables.yaml")


def apply_global_variables(content: str, source_dir: str) -> str:
    global_variables = load_global_variables(source_dir)
    return apply_variables(content, global_variables)


def apply_variables(content: str, variables: dict[str, str]) -> str:
    for name, value in variables.items():
        content = content.replace(f"@{{{name}}}", value)
    return content
