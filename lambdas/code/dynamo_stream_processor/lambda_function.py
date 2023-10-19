import os
import boto3
import json
import copy


from botocore.exceptions import ClientError


profiles = boto3.client('customer-profiles')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get("TABLE_NAME"))

def lambda_handler(event, context):
    print (event)

    records = event['Records']
    records_modify = []
    records_insert = []
    
    try:
        for rec in records:
            
            operation = rec["eventName"]
            if operation != "REMOVE":
                new_image  = rec["dynamodb"]["NewImage"]
                python_dict = {}
                for key, value in new_image.items():
                    python_dict[key] = value['S']
                
                print (python_dict)
                if operation == "MODIFY": records_modify.append(python_dict)
                if operation == "INSERT": records_insert.append(python_dict)

    
        update_inserted(records_insert)
        update_modified(records_modify)

    except ClientError as e:
        print(f"Error data: {e}")
        return {
            'error': f"Error data: {e}"
        }


def update_inserted(records):
    for rec in records:
        rec_copy = copy.deepcopy(rec)
        origin =  rec.get("OperationOrigin")

        if (origin != "Connect") :
            if rec.get("EventTimestamp"): del rec["EventTimestamp"]
            if rec.get("EventType"): del rec["EventType"]
            if rec.get("ObjectTypeName"): del rec["ObjectTypeName"]
            if (rec.get("GenderString") and rec.get("Gender")) : del rec["GenderString"]
            if rec.get("ProfileId"): del rec["ProfileId"]
            if rec.get("OperationOrigin"): del rec["OperationOrigin"]

            response = profiles.create_profile(**rec)
            if response.get("ProfileId"):
                if rec_copy.get("ProfileId"): table.delete_item(Key={"ProfileId": rec_copy.get("ProfileId")})
            print (response)



def update_modified(records):
    for rec in records:
        origin =  rec.get("OperationOrigin")
        if origin != "Connect":
            if rec.get("EventTimestamp"): del rec["EventTimestamp"]
            if rec.get("EventType"): del rec["EventType"]
            if rec.get("ObjectTypeName"): del rec["ObjectTypeName"]
            if (rec.get("GenderString") and rec.get("Gender")) : del rec["GenderString"]
            if rec.get("OperationOrigin"): del rec["OperationOrigin"]
            response = profiles.update_profile(**rec)
            print (response)