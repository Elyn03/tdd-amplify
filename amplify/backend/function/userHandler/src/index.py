import json
import os
import boto3
import uuid

def handler(event, context):
    if event['httpMethod'] == 'POST':
        add_user(event['body'])
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User added successfully'})
        }
    elif event['httpMethod'] == 'GET':
        user = get_user(event['queryStringParameters'])
        if user:
            return {
                'statusCode': 200,
                'body': json.dumps(user)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'message': 'Method not allowed'})
        }
    
def add_user(event):
    table_name = os.environ.get("STORAGE_USERTABLE_NAME", "UserTable")
    dynamodb = boto3.resource('dynamodb', region_name = "eu-west-1")
    table = dynamodb.Table(table_name)

    table.put_item(
        Item={
            'user_id': str(uuid.uuid4()),
            'name': event['name'],
            'email': event['email']
        }
    )

def get_user(event):
    table_name = os.environ.get("STORAGE_USERTABLE_NAME", "UserTable")
    dynamodb = boto3.resource('dynamodb', region_name = "eu-west-1")
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={
           'email': event['email']
        }
    )
    return response.get('Item')
