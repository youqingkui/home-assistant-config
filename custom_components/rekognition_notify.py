#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 17:52
# @Author  : youqingkui
# @File    : rekognition_notify.py
# @Desc    :



import boto3
from decimal import Decimal
import json
import urllib
import http.client

print('Loading function')

rekognition = boto3.client('rekognition')


def send_notify(payload):
    conn = http.client.HTTPConnection("maker.ifttt.com")
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
    }

    conn.request("POST", "/trigger/rich_notify/with/key/", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

# --------------- Helper Functions to call Rekognition APIs ------------------





def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    #table = boto3.resource('dynamodb').Table('MyTable')
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response


def index_faces(bucket, key):
    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    #rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
    response = rekognition.index_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}}, CollectionId="BLUEPRINT_COLLECTION")
    return response


# --------------- Main handler ------------------


def lambda_handler(event, context):
    '''Demonstrates S3 trigger that uses
    Rekognition APIs to detect faces, labels and index faces in S3 Object.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = detect_labels(bucket, key)
        for label in response['Labels']:
            print(label['Name'] + ' : ' + str(label['Confidence']))
            if label['Name'] in ['Human', 'People', 'Person', 'Face', 'Portrait']:
                pass

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
