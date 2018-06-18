# coding=utf-8

import base64
import hmac
from hashlib import sha1
import urllib
import time
import uuid

import requests
# from config.base import ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET

ALIYUN_ACCESS_KEY_ID = ''
ALIYUN_ACCESS_KEY_SECRET = ''

class AliyunMonitor:
    def __init__(self, url):
        self.access_id = ALIYUN_ACCESS_KEY_ID
        self.access_secret = ALIYUN_ACCESS_KEY_SECRET
        self.url = url

    # 签名
    def sign(self, accessKeySecret, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''

        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])    # 使用get请求方法
        key_byte = bytes(accessKeySecret + "&", encoding='utf8')
        h = hmac.new(key_byte, stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self, encodeStr):
        encodeStr = str(encodeStr)
        # 下面这行挺坑的，使用上面文章中的方法会在某些情况下报错，后面详细说明
        res = urllib.parse.quote(encodeStr.encode('utf-8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self, params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'Format': 'JSON',
            'Version': '2015-11-23',
            'AccessKeyId': self.access_id,
            'SignatureVersion': '1.0',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'Timestamp': timestamp,
        }
        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature

        # return parameters
        url = self.url + "/?" + urllib.parse.urlencode(parameters)
        return url


def send_email(email_address, subject, text):
    payload = {
        'Action': 'SingleSendMail',
        'AccountName': 'mail@mail.xxx.com',
        'ReplyToAddress': 'true',
        'AddressType': 0,
        'ToAddress': email_address,
        'FromAlias': 'TalkingCoder',
        'Subject': subject,
        'HtmlBody': text
    }

    aliyun = AliyunMonitor("http://dm.aliyuncs.com")
    url = aliyun.make_url(payload)

    request = requests.get(url)

    print(request.text)


if __name__=='__main__':
    send_email('test@test.com', '标题', '内容')