import json
import boto3
import os

def main(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    device_id = event.get("deviceId", "unknown")
    payload = json.dumps(event)

    # Save to S3
    s3.put_object(
        Bucket=os.environ['BUCKET_NAME'],
        Key=f"{device_id}.json",
        Body=payload
    )

    # Save to DynamoDB
    table.put_item(Item={
        "deviceId": device_id,
        "payload": payload
    })

    return {"status": "success"}
