import boto3
from moto import mock_dynamodb
from boto3.dynamodb.conditions import Key
import uuid

@mock.dynamodb
def test_add_user():
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.create_table(
        TableName='UserTable',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }

        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'email-index',
                'KeySchema': [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='UserTable')

    table.put_item(
        Item={
            'user_id': str(uuid.uuid4()),
            'name': 'John Doe',
            'email': 'test@teest.com'
        }
    )
