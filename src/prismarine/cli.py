from pathlib import Path
import logging as lg

import click

from prismarine.prisma_common import set_path
from prismarine.prisma_client import generate_client


@click.group()
@click.pass_context
@click.option(
    '--base', required=True, type=click.Path(exists=True),
    help="Primary Python path to use while searching for 'models' package"
)
@click.option(
    '--path', multiple=True, type=click.Path(exists=True),
    help='Additional Python path to use while generating the client'
)
@click.option(
    '--runtime', required=False,
    help="Cluster' package to use in runtime. If not provided, assume top-level"
)
@click.option(
    '--dynamo-access-module', required=False,
    help='''
Dynamo access module to use in runtime. If not provided, DefaultDynamoAccess access class from prismarine.runtime.dynamo_default will be used''',
)
@click.option(
    '--verbose', is_flag=True, help='Enable verbose logging'
)
def prismarine(ctx, path, base, runtime, verbose, dynamo_access_module):
    ctx.ensure_object(dict)
    lg.basicConfig(level=lg.DEBUG if verbose else lg.INFO)
    obj = ctx.obj
    paths = list(Path(p).resolve() for p in path) if path else []
    obj['BaseDir'] = Path(base)
    obj['Runtime'] = runtime
    obj['DynamoAccessModule'] = dynamo_access_module
    set_path(paths)


def main():
    prismarine.add_command(generate_client)
    prismarine()


if __name__ == '__main__':
    main()
