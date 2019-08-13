import boto3
import datetime
import json
import logging
import os
import time
import uuid

from boto3.dynamodb.conditions import Key, Attr


def Follow_User(event, context):
    print event['requestContext']['authorizer']['claims']['sub']
    print event['body']
    if 'body' not in event or event['body'] == '':
        logging.error("WARNING: Validation Failed: Empty request body.")
        raise Exception("Empty request received. Check all inputs.")

    data = json.loads(event['body'])
    if 'username' not in data:
        logging.error("WARNING: Validation Failed: No target phone number given.")
        raise Exception("Couldn't create phone record. Check all inputs.")

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FollowTable')  # Use env variable to store table name

    timestamp = datetime.datetime.utcnow().isoformat()
    item = {
        'username' : 'murali44',
        'followed_username': 'holly',
        'CreatedAt': timestamp,
        'UpdatedAt': timestamp,
    }

    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return add_cors_headers(response)


def Get_Followed_Users_List(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FollowTable') # Use env variable to store table name

    response = table.query(KeyConditionExpression=Key('username').eq('murali44'))
    items = response['Items']
    print items

    response = {
        "statusCode": 200,
        "body": json.dumps(items)
    }
    return add_cors_headers(response)


def add_cors_headers(response):
    response['headers'] = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    return response