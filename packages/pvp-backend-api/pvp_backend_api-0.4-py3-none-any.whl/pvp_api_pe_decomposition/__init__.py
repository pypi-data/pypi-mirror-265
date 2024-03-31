
import click
from .pe_decomposition import pe_decomposition_template

@click.command()
@click.option('--output', '-o', default='.', help='Output path for the template')
def cli(output):
    pe_decomposition_template(output)


if __name__ == "__main__":
    cli()


