import boto3
import datetime
import json
import logging
import os
import time
import uuid


def __dict_to_cognito(self, attributes, attr_map=None):
    if attr_map is None:
        attr_map = {}
    for k,v in attr_map.items():
        if v in attributes.keys():
            attributes[k] = attributes.pop(v)
    return [{'Name': key, 'Value': value} for key, value in attributes.items()]


def get_current_user(event, context):
    token = event['requestContext']['authorizer']['claims']['sub']

    cognito_client = boto3.client('cognito-idp')
    response = cognito_client.get_user(AccessToken=token)
    return response

def get_user(username=None, phone=None, email=None):
    print event['body']
    if 'body' not in event or event['body'] == '':
        logging.error("WARNING: Validation Failed: Empty request body.")
        raise Exception("Empty request received. Check all inputs.")

    data = json.loads(event['body'])

    cognito_client = boto3.client('cognito-idp')
    filter = ""

    if username:
        filter = "username = " + username
    elif phone:
        filter = "phone_number = " + phone
    elif email:
        filter = "email = " + email

    print "Cognito Filter:"
    print filter

    response = cognito_client.list_users(
        UserPoolId=os.environ['USERPOOL_ID'],
        AttributesToGet=['username','email','phone_number'],
        Filter=filter)

    print response

    return response