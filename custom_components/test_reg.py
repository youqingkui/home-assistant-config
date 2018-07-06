#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 12:03
# @Author  : youqingkui
# @File    : test_reg.py
# @Desc    :


import boto3

if __name__ == "__main__":
    fileName = '20180621/20180621064048.jpg'
    bucket = 'dafang'

    client = boto3.client('rekognition', 'ap-northeast-1')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': fileName}})
    print(response)
    print('Detected labels for ' + fileName)
    for label in response['Labels']:
        print(label['Name'] + ' : ' + str(label['Confidence']))