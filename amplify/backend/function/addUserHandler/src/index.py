import json
import os
import boto3
import uuid

def handler(event, context):
    table_name = os.environ.get("STORAGE_USERTABLE_NAME", "UserTable")
    dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
    table = dynamodb.Table(table_name)

    # Sécurité : utiliser get() pour éviter KeyError
    name = event.get('name')
    email = event.get('email')

    if not name or not email:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing name or email')
        }

    table.put_item(
        Item={
            'user_id': str(uuid.uuid4()),
            'name': name,
            'email': email
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('User added successfully!')
    }
