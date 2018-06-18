#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/17 08:15
# @Author  : youqingkui
# @File    : lambda_notify.py
# @Desc    :



import json
import urllib.parse
import boto3
import http.client

print('Loading function')

s3 = boto3.client('s3')

def send_notify(payload):
    conn = http.client.HTTPConnection("maker.ifttt.com")
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
    }

    conn.request("POST", "/trigger/rich_notify/with/key/cxqrds20FznBL5TjH4HggM", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def get_file_url(filename):
    file_arr = filename.split('/')
    date = file_arr[0]
    name = file_arr[-1]
    file_url = 'https://alexa.youqingkui.me/snapshot/%s/%s' % (date, name)
    return file_url


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    file_url = get_file_url(key)
    value1 = "dafang notify"
    if 'jpg' in key:
        payload = {"value2":file_url, "value1":value1}
    elif 'mp4' in key:
        payload = {"value3": file_url, "value1":value1}
    else:
        payload = {}
    payload = json.dumps(payload)
    try:
        send_notify(payload)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e