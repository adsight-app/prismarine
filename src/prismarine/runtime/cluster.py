class Cluster:
    prefix: str

    models = {}

    def __init__(self, prefix=''):
        self.prefix = prefix

    def model(
        self,
        *,
        PK: str,
        SK: str | None = None,
        table: str | None = None,
        name: str | None = None,
        alias: str | None = None
    ):
        def decorator(cls):
            self.models[name or cls.__name__] = {
                'cls': cls,
                'main': {'PK': PK, 'SK': SK},
                'table': table or self.prefix + (name or cls.__name__),
                'indexes': {},
                'class_name': cls.__name__
            }
            return cls

        return decorator

    def index(self, *, index: str, PK: str, SK: str | None = None):
        def decorator(cls):
            if not self.models.get(cls.__name__):
                raise Exception(
                    'Model not found. Index decorator must be placed above model decorator'
                )

            self.models[cls.__name__]['indexes'][index] = {'PK': PK, 'SK': SK}
            return cls

        return decorator
