import os
import boto3

from prismarine.runtime.dynamo_access import DynamoAccess


class MyDynamoAccess(DynamoAccess):
    def get_resource(self):
        return boto3.resource('dynamodb')

    def get_table(self, full_model_name: str):
        env = os.getenv('ENV')
        return self.get_resource().Table(f'{full_model_name}-{env}')


dynamoaccess = MyDynamoAccess()


def get_dynamo_access():
    return dynamoaccess
