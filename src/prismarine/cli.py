from pathlib import Path
import logging as lg
from importlib.metadata import version

import click

from prismarine.prisma_common import set_path
from prismarine.prisma_client import generate_client


@click.group()
@click.pass_context
@click.option(
    '--path', multiple=True, type=click.Path(exists=True),
    help='Additional Python path to use'
)
@click.option(
    '--verbose', is_flag=True, help='Enable verbose logging'
)
def prismarine(ctx, path, verbose):
    ctx.ensure_object(dict)
    lg.basicConfig(level=lg.DEBUG if verbose else lg.INFO)
    paths = list(Path(p).resolve() for p in path) if path else []
    set_path(paths)


@prismarine.command(
    name='generate-client',
    help='Generate a Prismarine client сщву for a given cluster package'
)
@click.option(
    '--base', required=True, type=click.Path(exists=True),
    help="Primary Python path to use while searching for 'models' package"
)
@click.option(
    '--runtime', required=False,
    help='Parent package for models to use in runtime. If not provided, assume top-level'
)
@click.option(
    '--dynamo-access-module', required=False,
    help='''
Dynamo access module to use in runtime. If not provided, DefaultDynamoAccess access class from prismarine.runtime.dynamo_default will be used'''
)
@click.argument('cluster_package')
def generate_client_cmd(base, runtime, dynamo_access_module, cluster_package):
    base_dir = Path(base)

    generate_client(
        base_dir,
        cluster_package,
        runtime,
        dynamo_access_module
    )


@prismarine.command(
    name='version',
    help='Print the version of Prismarine'
)
def version_cmd():
    click.echo(version('prismarine'))


def main():
    prismarine()


if __name__ == '__main__':
    main()
