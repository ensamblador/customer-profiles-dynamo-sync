import os
import boto3
import json
from base64 import b64decode
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print (event)
    records = event['Records']
    records_plaintext = []
    try:
        for rec in records:
            encrypted_data = rec['kinesis']['data']
            print ("data:",encrypted_data)
            encrypted_data = b64decode(encrypted_data)
            print ("decoded data:",encrypted_data)

            records_plaintext.append(json.loads(encrypted_data))
        
        write_elems(os.environ.get("TABLE_NAME"), records_plaintext)
        
        return True

    except ClientError as e:
        # Handle decryption errors
        print(f"Error decrypting data: {e}")
        return {
            'error': 'Failed to decrypt data'
        }


def write_elems(table_name, items_array):
    for itm in items_array:
        profile = itm["Object"]
        profile["EventType"] = itm["EventType"]
        profile["ObjectTypeName"] = itm["ObjectTypeName"]
        profile["DomainName"] = itm["DomainName"]
        profile["EventTimestamp"] = itm["EventTimestamp"]
        profile["EventTimestamp"] = itm["EventTimestamp"]
        profile["OperationOrigin"] = "Connect"
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for itm in items_array:
            res = batch.put_item(Item=itm["Object"])