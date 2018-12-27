import os
import time
import json
import requests

from flask import Flask, request
from werkzeug.utils import secure_filename

import boto3

UPLOAD_FOLDER = '/data/minio/dafang'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mov', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

s3 = boto3.client('s3')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_today():
    today_date = time.strftime("%Y%m%d", time.localtime())
    return today_date

def mkdir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def ifttt_notify(date, file_name):
    ifttt_token = os.getenv('ifttt_token')
    url = "https://maker.ifttt.com/trigger/rich_notify/with/key/%s" % ifttt_token
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
    }
    payload = {"value1":"dafang notify"}

    file_url = "https://minio.youqingkui.me/dafang/%s/%s" % (date, file_name)
    if 'jpg' in file_name:
        payload["value1"] = "dafang notify with image"
        payload['value3'] = file_url
    elif "mp4" in file_name:
        payload["value1"] = "dafang notify with video"
        payload['value2'] = file_url
    payload = json.dumps(payload)
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "error"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return "error"
        if file and allowed_file(file.filename):
            today_date = get_today()
            filename = secure_filename(file.filename)
            save_dir = os.path.join(app.config['UPLOAD_FOLDER'], today_date)
            mkdir(save_dir)
            file_path = os.path.join(save_dir, filename)
            file.save(file_path)
            ifttt_notify(today_date, filename)

            s3_name = '%s/%s' % (today_date, filename)
            s3.upload_file(file_path, 'dafang', s3_name)
            return "ok"

@app.route('/script_do')
def script_do():
    url = "http://192.168.31.238:8123/api/services/script/open_door_shell"

    querystring = {"api_password": "xz5xwK3WXhbPKUjW"}

    payload = ""
    headers = {}
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    return response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0')
