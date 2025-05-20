def build_dynamo_tables(prefix, cluster):
    'Returns: (Full Table Name with Prefix, EasySAM Table Definition)'

    result = {}

    for _, data in cluster.models.items():
        table_name = data['table']
        short_name = table_name.replace(prefix, '')

        main = data['main']

        attributes = {}
        indices = []

        if 'PK' not in main or not main['PK']:
            raise UserWarning(f'PK is required for table {table_name}')

        attributes[main['PK']] = {'hash': True}

        if 'SK' in main and main['SK']:
            attributes[main['SK']] = {'range': True}

        for index_name, index in data['indexes'].items():
            sam_index = {'name': index_name}
            index_attributes = []

            if 'PK' not in index or not index['PK']:
                raise UserWarning(f'PK is required for index {index} in table {table_name}')

            index_attributes.append({'name': index['PK'], 'hash': True})

            if index['PK'] not in attributes:
                attributes[index['PK']] = {}

            if 'SK' in index and index['SK']:
                if index['SK'] not in attributes:
                    attributes[index['SK']] = {}

                index_attributes.append({'name': index['SK'], 'range': True})

            sam_index['attributes'] = index_attributes
            indices.append(sam_index)

        def named_dict_to_item(name, data):
            result = {'name': name}
            result.update(data)
            return result

        result[short_name] = {
            'attributes': list(named_dict_to_item(k, v) for k, v in attributes.items()),
        }

        if indices:
            result[short_name]['indices'] = indices

    return result
