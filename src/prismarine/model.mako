class ${ModelClass}(Model):
    table_name = '${TableName}'
    PK = '${PartitionKey}'
    % if SortKey:
    SK = '${SortKey}'
    % endif

    % for line in DtoLines:
    ${line}
    % endfor

    % if SortKey:
    @staticmethod
    def list(*, ${snake(PartitionKey)}: str, **kwargs) -> List[${Model}]:
        return _query(dynamo, ${ModelClass}.table_name, {${ModelClass}.PK: ${snake(PartitionKey)}}, **kwargs)
    % endif

    @staticmethod
    % if SortKey:
    def get(*, ${snake(SortKey)}: str, ${snake(PartitionKey)}: str, default: ${Model} | EllipsisType = ..., **kwargs) -> ${Model}:
        item = _get_item(dynamo, ${ModelClass}.table_name, {${ModelClass}.PK: ${snake(PartitionKey)}, ${ModelClass}.SK: ${snake(SortKey)}}, default, **kwargs)
    % else:
    def get(*, ${snake(PartitionKey)}: str, default: ${Model} | EllipsisType = ..., **kwargs) -> ${Model}:
        item = _get_item(dynamo, ${ModelClass}.table_name, {${ModelClass}.PK: ${snake(PartitionKey)}}, default, **kwargs)
    % endif
        if not item:
        % if SortKey:
            raise DbNotFound(f'Item was not found in {${ModelClass}.table_name} with params ${snake(PartitionKey)}={${snake(PartitionKey)}}, ${snake(SortKey)}={${snake(SortKey)}}')
        % else:
            raise DbNotFound(f'Item was not found in {${ModelClass}.table_name} with params ${snake(PartitionKey)}={${snake(PartitionKey)}}')
        % endif
        return item

    @staticmethod
    def put(${snake(Model)}: ${Model}, **kwargs) -> ${Model}:
        _put_item(dynamo, ${ModelClass}.table_name, ${snake(Model)}, **kwargs)
        return ${snake(Model)}

    @staticmethod
    % if SortKey:
    def update(${snake(Model)}: UpdateDTO, *, ${snake(PartitionKey)}: str, ${snake(SortKey)}: str, default: ${Model} | EllipsisType = ...) -> ${Model}:
        initial = ${ModelClass}.get(${snake(SortKey)}=${snake(SortKey)}, ${snake(PartitionKey)}=${snake(PartitionKey)}, default=default)
        _update(dynamo, ${ModelClass}.table_name, {${ModelClass}.PK: ${snake(PartitionKey)}, ${ModelClass}.SK: ${snake(SortKey)}}, without(${snake(Model)}, [${ModelClass}.PK, ${ModelClass}.SK]))
        return {**initial, **${snake(Model)}}
    % else:
    def update(${snake(Model)}: UpdateDTO, *, ${snake(PartitionKey)}: str, default: ${Model} | EllipsisType = ...) -> ${Model}:
        initial = ${ModelClass}.get(${snake(PartitionKey)}=${snake(PartitionKey)}, default=default)
        _update(dynamo, ${ModelClass}.table_name, {${ModelClass}.PK: ${snake(PartitionKey)}}, without(${snake(Model)}, [${ModelClass}.PK]))
        return {**initial, **${snake(Model)}}
    % endif

    @staticmethod
    % if SortKey:
    def save(updated: ${Model}, *, original: ${Model} | None = None) -> ${Model}:
        _save(dynamo, ${ModelClass}.table_name, kv={${ModelClass}.PK: updated[${ModelClass}.PK], ${ModelClass}.SK: updated[${ModelClass}.SK]}, updated=updated, original=original)
        return updated
    % else:
    def save(updated: ${Model}, *, original: ${Model} | None = None) -> ${Model}:
        _save(dynamo, ${ModelClass}.table_name, kv={${ModelClass}.PK: updated[${ModelClass}.PK]}, updated=updated, original=original)
        return updated
    % endif

    @staticmethod
    % if SortKey:
    def delete(*, ${snake(SortKey)}: str, ${snake(PartitionKey)}: str, **kwargs):
        _delete(dynamo, ${ModelClass}.table_name, {${ModelClass}.PK: ${snake(PartitionKey)}, ${ModelClass}.SK: ${snake(SortKey)}}, **kwargs)
    % else:
    def delete(*, ${snake(PartitionKey)}: str, **kwargs):
        _delete(dynamo, ${ModelClass}.table_name, {${ModelClass}.PK: ${snake(PartitionKey)}}, **kwargs)
    % endif

    @staticmethod
    def scan(**kwargs) -> List[${Model}]:
        return _scan(dynamo, ${ModelClass}.table_name, **kwargs)

    % for index in Indexes:
    class ${pascal(index['name'])}:
        PK = '${index['PartitionKey']}'
        % if index['SortKey']:
        SK = '${index['SortKey']}'
        % endif
        
        @staticmethod
        def list(*, ${snake(index['PartitionKey'])}: str, limit: int | None = None, direction: Literal['ASC', 'DESC'] = 'ASC') -> List[${Model}]:
            return _query(dynamo, ${ModelClass}.table_name, {${ModelClass}.${pascal(index['name'])}.PK: ${snake(index['PartitionKey'])}}, index='${index['name']}', limit=limit, direction=direction)

        % if index['SortKey']:
        @staticmethod
        def get(*, ${snake(index['PartitionKey'])}: str, ${snake(index['SortKey'])}: str) -> ${Model}:
            items = _query(dynamo, ${ModelClass}.table_name, {${ModelClass}.${pascal(index['name'])}.PK: ${snake(index['PartitionKey'])}, ${ModelClass}.${pascal(index['name'])}.SK: ${snake(index['SortKey'])}}, index='${index['name']}')
            if not items:
                raise DbNotFound(f'Item was not found in {${ModelClass}.table_name} with params ${snake(index['PartitionKey'])}={${snake(index['PartitionKey'])}}, ${snake(index['SortKey'])}={${snake(index['SortKey'])}}')

            return items[0]
        % endif
    % endfor