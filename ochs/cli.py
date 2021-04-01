import click

from ochs.builder.compiler import compile_source
from ochs.utils.log import setup_logger


@click.group()
@click.option("--debug/--no-debug", default=False)
def ochs(debug: bool) -> None:
    setup_logger(debug)


@ochs.command()
@click.argument("source_directory")
@click.argument("target_directory")
def build(source_directory: str, target_directory: str) -> None:
    compile_source(source_directory, target_directory)
