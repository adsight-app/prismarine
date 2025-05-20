import importlib
import logging as lg
import sys
from pathlib import Path


def set_path(path_dir_list: list[Path]):
    for path_dir in path_dir_list:
        r_path_dir = Path(path_dir).resolve()
        lg.info(f'Adding path: {r_path_dir}')
        sys.path.append(str(r_path_dir))


def get_cluster(base_dir: Path, cluster_package: str):
    r_base_dir = base_dir.resolve()
    lg.info(f'Using base: {r_base_dir}')
    sys.path.append(str(r_base_dir))
    lg.debug(f'Set Python path: {sys.path}')
    models = importlib.import_module(f'{cluster_package}.models')

    # NB: Reload is needed to handle the same file structure for multiple clusters
    importlib.reload(models)
    lg.debug(f'Removing base: {r_base_dir}')
    sys.path.remove(str(r_base_dir))

    for name in dir(models):
        obj = getattr(models, name)
        if isinstance(obj, models.Cluster):
            lg.info(f'Cluster found: {obj.prefix}')
            return obj

    raise UserWarning('Cluster not found')
