import boto3
import datetime
import json
import os
import uuid

from boto3.dynamodb.conditions import Key, Attr


followtable = os.environ['FOLLOWTABLE']
videotable = os.environ['VIDEOTABLE']

# *********** APIs ************

def Upload_Video(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']
    request = json.loads(event["body"])

    table = boto3.resource('dynamodb').Table(videotable)

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

    s3Client = boto3.client('s3')
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
        "body": body
    }

    return add_cors_headers(response)


def Delete_Video(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']
    request = json.loads(event["body"])

    table = boto3.resource('dynamodb').Table(videotable)

    table.delete_item(
        Key={
            'username': current_user,
            'filename': request['filename']
        }
    )

    # Delete from S3 here
    s3Client = boto3.client('s3')

    response = {
        "statusCode": 200,
        "body": ''
    }

    return add_cors_headers(response)


def Get_user_videos(user):
    
    table = boto3.resource('dynamodb').Table(videotable)
    videos = table.query(KeyConditionExpression=Key('username').eq(user))
    return videos

def Get_Followed_User_Videos_List(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(followtable)

    videolist = []

    response = table.query(KeyConditionExpression=Key('username').eq(current_user))
    users = response['Items']

    for user in users:
        videos = Get_user_videos(user['followed_username'])
        for x in range(videos['Count']):
            item = {"username": videos['Items'][x]['username'], "filename": videos['Items'][x]['filename']}
            videolist.append(item)

    response = {
        "statusCode": 200,
        "body": json.dumps(videolist)
    }

    return add_cors_headers(response)


def add_cors_headers(response):
    response['headers'] = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    return response
