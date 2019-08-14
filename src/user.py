import boto3
import datetime
import json
import logging
import os
import time
import uuid

from boto3.dynamodb.conditions import Key, Attr

# ************ Util Function ************

def __dict_to_cognito(self, attributes, attr_map=None):
    if attr_map is None:
        attr_map = {}
    for k,v in attr_map.items():
        if v in attributes.keys():
            attributes[k] = attributes.pop(v)
    return [{'Name': key, 'Value': value} for key, value in attributes.items()]


def get_current_user(token=None):
    cognito_client = boto3.client('cognito-idp')
    response = cognito_client.get_user(AccessToken=token)
    return response

def get_user(username=None, phone=None, email=None):
    cognito_client = boto3.client('cognito-idp')
    filter = ""

    if username:
        filter = "username = " + "\"" + username + "\""
    elif phone:
        filter = "phone_number = " + "\"" + phone + "\""
    elif email:
        filter = "email = " + "\"" + email + "\""

    print "Cognito Filter:"
    print filter

    response = cognito_client.list_users(
        UserPoolId=os.environ['USERPOOL_ID'],
        AttributesToGet=['preferred_username'],
        Filter=filter)

    print response
    user = response["Users"][0]['Username']

    return user


# *********** APIs ************

def Follow_User(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']

    if 'body' not in event or event['body'] == '':
        logging.error("WARNING: Validation Failed: Empty request body.")
        raise Exception("Empty request received. Check all inputs.")

    data = json.loads(event['body'])
    user = None

    if 'username' in data:
        user = get_user(username=data['username'])
    elif 'phone' in data:
        user = get_user(phone=data['phone'])
    elif 'email' in data:
        user = get_user(email=data['email'])
    else:
        logging.error("WARNING: Validation Failed: Empty request body.")
        raise Exception("Empty request received. Check all inputs.")

    # First check if the user exisits
    user = get_user(username=data['username'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FollowTable')  # Use env variable to store table name

    timestamp = datetime.datetime.utcnow().isoformat()
    item = {
        'username' : current_user,
        'followed_username': user,
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


def Unfollow_User(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']

    if 'body' not in event or event['body'] == '':
        logging.error("WARNING: Validation Failed: Empty request body.")
        raise Exception("Empty request received. Check all inputs.")

    data = json.loads(event['body'])
    user_to_unfollow = None

    if 'username' in data:
        user_to_unfollow = get_user(username=data['username'])
    elif 'phone' in data:
        user_to_unfollow = get_user(phone=data['phone'])
    elif 'email' in data:
        user_to_unfollow = get_user(email=data['email'])
    else:
        logging.error("WARNING: Validation Failed: Empty request body.")
        raise Exception("Empty request received. Check all inputs.")

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FollowTable')  # Use env variable to store table name

    response = table.delete_item(Key={'username': current_user, 'followed_username': user_to_unfollow})

    # create a response
    response = {
        "statusCode": 200,
        "body": user_to_unfollow
    }

    return add_cors_headers(response)


def Get_Followed_Users_List(event, context):
    current_user = event['requestContext']['authorizer']['claims']['cognito:username']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FollowTable') # Use env variable to store table name

    response = table.query(KeyConditionExpression=Key('username').eq(current_user))
    items = response['Items']

    for item in items:
        del item['username']
        del item['CreatedAt']
        del item['UpdatedAt']

    response = {
        "statusCode": 200,
        "body": json.dumps(items)
    }
    return add_cors_headers(response)


def add_cors_headers(response):
    response['headers'] = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
    return response

