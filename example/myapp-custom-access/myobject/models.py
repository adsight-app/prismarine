from typing import TypedDict, NotRequired
from prismarine.runtime import Cluster


c = Cluster('MyDatabase')


@c.model(PK='Foo', SK='Bar')
class Item(TypedDict):
    Foo: str
    Bar: str
    Baz: NotRequired[str]
