import json
import os
import boto3
import uuid

def handler(event, context):
    table_name = os.environ.get("STORAGE_USERTABLE_NAME", "UserTable")
    dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
    table = dynamodb.Table(table_name)

    email = event.get('email')
    if not email:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'email' in event input"})
        }

    try:
        response = table.get_item(
            Key={
                'email': email
            }
        )
        item = response.get('Item')
        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "User not found"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
