# Prismarine - DynamoDB ORM

Prismarine is a Pythonic ORM for DynamoDB, designed to simplify interactions with DynamoDB by providing a structured and Python-friendly interface. It leverages Python's type hinting and decorators to define models, which are then used to generate client code for database operations.

Key features include:
- **Model Definition**: Models are defined using Python's `TypedDict` and are decorated with the `Cluster.model` decorator to specify primary and sort keys.
- **Automatic Client Generation**: The `prismarine_client.py` file is auto-generated, containing classes and methods for interacting with DynamoDB tables based on the defined models.
- **Easy Integration**: The generated client code integrates seamlessly with existing Python applications, providing methods for common database operations.

Prismarine aims to streamline the development process by reducing boilerplate code and ensuring that database interactions are type-safe and maintainable.

Prismarine works best with [EasySAM](https://github.com/adsight-app/easysam).

## Installation

```bash
pip install prismarine
```

## Quick Overview

### Expected Directory Structure:

```
<base-path>/
  <package-name>/
    - models.py
    - db.py
    - prismarine_client.py // Auto-generated
```

Models are defined in the `models.py` file. Each model is a `TypedDict`, decorated with the `Cluster.model` decorator.

The `Cluster` class is used to group extension models together. It also sets a prefix for the table names.

```python
from typing import TypedDict, NotRequired
from prismarine import Cluster

c = Cluster('TapgameExample')

@c.model(PK='Foo', SK='Bar')
class Team(TypedDict):
    Foo: str
    Bar: str
    Baz: NotRequired[str]
```

If we place this code in `<base-path>/<package-name>/models.py` and the following command is run, it will generate a `prismarine_client.py` file in the same directory:

```pwsh
python .\tools\prismarine\cli.py --base <base-path> generate-client <package-name>
```

The `prismarine_client.py` file will contain the following code:

```python
class TeamModel(Model):
    table_name = 'TapgameExampleTeam'
    PK = 'Foo'
    SK = 'Bar'

    class UpdateDTO(TypedDict, total=False):
        Foo: str
        Bar: str
        Baz: NotRequired[str]

    @staticmethod
    def list(*, foo: str) -> List[Team]:
        ...

    @staticmethod
    def get(*, bar: str, foo: str, default: Team | EllipsisType = ...) -> Team:
        ...

    @staticmethod
    def put(team: Team) -> Team:
        ...

    @staticmethod
    def update(
        team: UpdateDTO, *, foo: str, bar: str, default: Team | EllipsisType = ...
    ) -> Team:
        ...

    @staticmethod
    def save(updated: Team, *, original: Team | None = None) -> Team:
        ...

    @staticmethod
    def delete(*, bar: str, foo: str):
        ...

    @staticmethod
    def scan() -> List[Team]:
        ...
```

As you can see, the `TeamModel` class has static methods for all the CRUD operations. The `UpdateDTO` class is similar to the `Team` class, but all fields are optional.

### Creating a `db.py` File

Now, let's create a `db.py` file in the same directory:

```python
import example.prismarine_client as pc

class TeamModel(pc.TeamModel):
    pass
```

Although you can import and use `prismarine_client.py` directly, it is recommended to create a `db.py` file that imports the generated client and extends it with your own methods.

You can now use the `TeamModel` class in your code:

```python
from sam.common.example.db import TeamModel
from sam.common.prismarine import DbNotFound

# Create a new team
new_team = TeamModel.put({'Foo': 'foo', 'Bar': 'bar', 'Baz': 'baz'})

# List teams by a primary key
teams_by_foo = TeamModel.list(foo='foo')

# Get a team
try:
    team = TeamModel.get(foo='foo', bar='bar')
except DbNotFound:
    print('Team not found')

# Update a team
updated_team = TeamModel.update(
    {'Baz': 'new_baz'},
    foo='foo',
    bar='bar'
)

# List all teams
all_teams = TeamModel.scan()

# Delete a team
TeamModel.delete(foo='foo', bar='bar')
```

You may notice that Prismarine mostly requires named arguments. This ensures that changes to field names do not cause silent code failures. For example, if the Sort Key name is changed, all usages of `get` and `update` methods will break and be highlighted by the IDE and linter. This approach also makes the code more readable.

## Advanced Usage

### `model` Decorator

Aside from the `PK` and `SK` arguments, the `Cluster.model` decorator also accepts `table` and `name` arguments. `table` sets a full custom table name, while `name` sets a custom model name. For example, if the `Cluster` has a prefix `TapgameExample`, by default the `Team` model will have the table name `TapgameExampleTeam`. If we set `name='Custom'`, the table name will be `TapgameExampleCustom`. And if we set `table='CustomTable'`, the table name will simply be `CustomTable`, without the prefix.

### `index` Decorator

`index` decorators must be used *before* the `model` decorator.

The `Cluster.index` decorator is used to define a secondary index. It accepts `PK`, `SK`, and `index` arguments.

```python
@c.index(index='by-bar', PK='Bar', SK='Foo')
@c.model(PK='Foo', SK='Bar')
class Team(TypedDict):
    Foo: str
    Bar: str
    Baz: NotRequired[str]
```

This will add a subclass `ByBar` to the `TeamModel` class:

```python
class TeamModel(Model):
    ...

    class ByBar:
        PK = 'Bar'
        SK = 'Foo'

        @staticmethod
        def list(
            *,
            bar: str,
            limit: int | None = None,
            direction: Literal['ASC', 'DESC'] = 'ASC'
        ) -> List[Team]:
            ...

        @staticmethod
        def get(*, bar: str, foo: str) -> Team:
            ...
```