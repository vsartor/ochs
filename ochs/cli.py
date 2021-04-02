import click

from ochs.builder.compiler import compile_source
from ochs.utils.log import setup_logger


@click.group()
@click.option("--silent/--no-silent", default=False)
def ochs(silent: bool) -> None:
    setup_logger(silent)


@ochs.command()
@click.argument("source_directory")
@click.argument("target_directory")
def build(source_directory: str, target_directory: str) -> None:
    compile_source(source_directory, target_directory)
