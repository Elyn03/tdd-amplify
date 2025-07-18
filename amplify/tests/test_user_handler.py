import boto3
import sys
import os
from moto import mock_dynamodb

sys.path.insappend(os.path.abspath("./amplify/backend/function/userHandler/src"))
# import index from handler

@mock.dynamodb
def test_add_and_get_user_by_email():
    # 1 simule dynamodb
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

    # 2 
    handler.TABLE_NAME = 'UserTable'
    handler.table = dynamodb.Table('UserTable')

    # 3 add user
    table.put_item(
        Item={
            'user_id': '123dsqdsq',
            'name': 'John Doe',
            'email': 'test@teest.com'
        }
    )

    response = table.query(
        IndexName='email-index',
        KeyConditionExpression=Key('email').eq('test@teest.com')
    )

    items = response.get('Items', [])
    assert len(items) == 1
    assert items[0]['user_id'] == '123dsqdsq'
    assert items[0]['name'] == 'John Doe'
