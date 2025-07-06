import json
import os
import boto3
import uuid

def handler(event, context):
    table_name = os.environ.get("STORAGE_USERTABLE_NAME", "UserTable")
    dynamodb = boto3.resource('dynamodb', region_name = "eu-west-1")
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={
           'email': event['email']
        }
    )
    return response.get('Item')