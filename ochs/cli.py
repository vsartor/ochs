import click

from ochs.builder.compiler import compile_source
from ochs.flags import enable_prod_flag
from ochs.utils.log import setup_logger


@click.group()
@click.option("--silent/--no-silent", default=False)
def ochs(silent: bool) -> None:
    setup_logger(silent)


@ochs.command()
@click.argument("source_directory")
@click.argument("target_directory")
@click.option("-p", "--prod", is_flag=True)
def build(source_directory: str, target_directory: str, prod: bool) -> None:
    if prod:
        enable_prod_flag()
    compile_source(source_directory, target_directory)
