import json
import uuid
import boto3
from boto3 import resource
import datetime
import os


# *********** APIs ************

def Upload_Video(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']

    print('generate_s3_presigned_url function executing')
    print('Event: '+json.dumps(event))
    print('request body: '+event['body'])

    request = json.loads(event["body"])

    dynamodb_resource = resource('dynamodb')
    table = dynamodb_resource.Table(os.environ['VIDEOTABLE'])

    timestamp = datetime.datetime.utcnow().isoformat()
    filename = request['filename'] + '-' + uuid.uuid4().hex

    table.put_item(
        Item = {
            'username': current_user,
            'filename': filename,
            'processingStatus': 'inprogress',
            'creationDate': timestamp
        }
    )

    # Get s3 client
    s3Client = boto3.client('s3')

   
     #fields = {'ContentType': 'application/octet-stream'}
     #url = s3Client.generate_presigned_post(
     #    os.environ['S3BUCKET'],
     #    filename,
     #    Fields=fields,
      #   ExpiresIn=900)

    url = s3Client.generate_presigned_url(
                ClientMethod = 'put_object',
                Params = {
                    'Bucket': os.environ['S3BUCKET'],
                    'Key': filename,
                    'ContentType': 'video/mp4'
                },
                ExpiresIn = 3600,
                HttpMethod='PUT'
            )

    body =  json.dumps({
            'upload_url' : url
        })

    response = {
        "statusCode": 200,
        "body": body,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*", # required for cors support
            "Access-Control-Allow-Credentials": "true" # required for cookies, authorization headers with https
        }
    }

    return response


def Delete_Video(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']
    request = json.loads(event["body"])

    dynamodb_resource = resource('dynamodb')
    table = dynamodb_resource.Table(os.environ['VIDEOTABLE'])

    table.delete_item(
        Key={
            'username': current_user,
            'filename': request['filename']
        }
    )

    # Delete from S3
    s3Client = boto3.client('s3')

    response = {
        "statusCode": 200,
        "body": '',
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*", # required for cors support
            "Access-Control-Allow-Credentials": "true" # required for cookies, authorization headers with https
        }
    }

    return response


def Get_Followed_User_Videos_List(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']
    request = json.loads(event["body"])