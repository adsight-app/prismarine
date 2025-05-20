from types_boto3_dynamodb import ServiceResource
from types_boto3_dynamodb.service_resource import Table


class DynamoAccess:
    def get_resource(self) -> ServiceResource: ...
    def get_table(self, full_model_name: str) -> Table: ...
