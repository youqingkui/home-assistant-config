#!/usr/bin/env bash

FILE=`date +%Y%m%d%H%M%S.mp4`
SAVE_DIR="/data/minio/dafang/video"
SUB_DIR="$(date +%Y%m%d)"
RECORDING_PATH="$SAVE_DIR/$SUB_DIR/$FILE"
VIDEO_IP="rtsp://192.168.31.187:8554/unicast"
notify_file="https://minio.youqingkui.me/dafang/video/$SUB_DIR/$FILE"


if [ ! -d "$SAVE_DIR/$SUB_DIR" ]; then
      mkdir -p "$SAVE_DIR/$SUB_DIR"
fi

if ffmpeg -stimeout 10000000 -rtsp_transport tcp -y -i "$VIDEO_IP" -vcodec copy -c:a aac -strict experimental -t 15 "$RECORDING_PATH"; then

    curl -X POST \
      https://maker.ifttt.com/trigger/rich_notify/with/key/cxqrds20FznBL5TjH4HggM \
      -H 'Cache-Control: no-cache' \
      -H 'Content-Type: application/json' \
      -H 'Postman-Token: b1ac6145-c94d-4354-b2f2-a8025f28eebd' \
      -d '{
        "event":"rich_notify",
        "value1":"hello",
        "value2":"'$notify_file'",
        "value3":"'$notify_file'"}'

    curl -X POST \
      https://api.pushbullet.com/v2/pushes \
      -H 'Access-Token: o.qG1UpoJZEuCGsizto1v6RCwinkO77Jlg' \
      -H 'Content-Type: application/json' \
      -H 'cache-control: no-cache' \
      -d '{
        "type":"file",
        "body": "video",
        "file_name":"'$FILE'",
        "file_type": "video/mp4",
        "file_url":"'$notify_file'"
    }'
fi
