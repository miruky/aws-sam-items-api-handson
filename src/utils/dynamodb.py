import os

import boto3


def get_table():
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT")

    if endpoint_url:
        dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=endpoint_url,
            region_name=os.environ.get("AWS_REGION", "ap-northeast-1"),
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy"
        )
    else:
        dynamodb = boto3.resource("dynamodb")

    return dynamodb.Table(os.environ["TABLE_NAME"])

