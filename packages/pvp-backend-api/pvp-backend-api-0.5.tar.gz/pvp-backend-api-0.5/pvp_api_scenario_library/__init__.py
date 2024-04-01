
import click
import os
from .scenario_library import scenario_library_template

@click.command()
@click.option('--output', '-o', default='.', help='Output path for the template')
def cli(output):
    scenario_library_template(output)


if __name__ == "__main__":
    cli()


