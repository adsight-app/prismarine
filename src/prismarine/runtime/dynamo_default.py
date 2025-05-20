import boto3

from prismarine.runtime.dynamo_access import DynamoAccess


class DefaultDynamoAccess(DynamoAccess):
    def get_resource(self):
        return boto3.resource('dynamodb')

    def get_table(self, full_model_name: str):
        return self.get_resource().Table(full_model_name)


dynamoaccess = DefaultDynamoAccess()


def get_dynamo_access():
    return dynamoaccess
