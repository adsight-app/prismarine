from pathlib import Path
import textwrap
import uuid

import pytest

from prismarine.prisma_client import build_client
from prismarine.prisma_common import get_cluster


def _write_models(tmp_path, body: str, package_name: str | None = None):
    base_dir = tmp_path / 'project'
    pkg = package_name or f'app_{uuid.uuid4().hex}'
    package_dir = base_dir / pkg
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / '__init__.py').write_text('')
    (package_dir / 'models.py').write_text(textwrap.dedent(body))
    return base_dir, pkg


def _stub_version(monkeypatch):
    monkeypatch.setattr('prismarine.prisma_client.version', lambda _: '0.0.0-test')


def test_build_client_with_typeddict_models(tmp_path, monkeypatch):
    body = '''
from typing import TypedDict
from prismarine.runtime import Cluster

cluster = Cluster('UnitTest')


@cluster.model(PK='Foo', SK='Bar')
class TypedItem(TypedDict):
    Foo: str
    Bar: str
    Baz: str
'''
    base_dir, cluster_package = _write_models(tmp_path, body)
    _stub_version(monkeypatch)
    cluster = get_cluster(base_dir, cluster_package)

    content = build_client(
        cluster,
        Path(base_dir),
        runtime=None,
        access_module=None,
        extra_imports=[],
        model_library='typed_dict'
    )

    assert 'class UpdateDTO(TypedDict, total=False):' in content
    assert '_build_pydantic_update_model' not in content


@pytest.mark.parametrize('extra_field', ['', "    Baz: int | None = None\n"])
def test_build_client_with_pydantic_models(tmp_path, monkeypatch, extra_field):
    body = f'''
from pydantic import BaseModel, Field
from prismarine.runtime import Cluster

cluster = Cluster('UnitTest')


@cluster.model(PK='Foo', SK='Bar')
class PydItem(BaseModel):
    Foo: str
    Bar: str
{extra_field or "    Baz: int | None = Field(default=None, alias='baz_field')"}
'''
    base_dir, cluster_package = _write_models(tmp_path, body)
    _stub_version(monkeypatch)
    cluster = get_cluster(base_dir, cluster_package)

    content = build_client(
        cluster,
        Path(base_dir),
        runtime=None,
        access_module=None,
        extra_imports=[],
        model_library='pydantic'
    )

    assert '_build_pydantic_update_model' in content
    assert 'UpdateDTO(TypedDict, total=False)' not in content
    assert '_load_model' in content


def test_pydantic_mode_rejects_typeddict_models(tmp_path, monkeypatch):
    body = '''
from typing import TypedDict
from prismarine.runtime import Cluster

cluster = Cluster('UnitTest')


@cluster.model(PK='Foo')
class Item(TypedDict):
    Foo: str
'''
    base_dir, cluster_package = _write_models(tmp_path, body)
    _stub_version(monkeypatch)
    cluster = get_cluster(base_dir, cluster_package)

    with pytest.raises(TypeError):
        build_client(
            cluster,
            Path(base_dir),
            runtime=None,
            access_module=None,
            extra_imports=[],
            model_library='pydantic'
        )
