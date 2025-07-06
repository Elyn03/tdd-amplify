import boto3
from moto import mock_dynamodb
from boto3.dynamodb.conditions import Key

@mock.dynamodb
def test_get_user_by_email():
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

    response = table.query(
        IndexName='email-index',
        KeyConditionExpression=Key('email').eq('test@teest.com')
    )

    items = response.get('Items', [])
    assert len(items) == 1
    assert items[0]['user_id'] == '123'
    assert items[0]['name'] == 'John Doe'
