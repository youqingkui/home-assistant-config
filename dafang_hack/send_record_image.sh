#!/bin/sh

PIDFILE="/run/send_record_image.pid"
FILE=`date +%Y%m%d%H%M%S.jpg`
SAVE_DIR="/system/sdcard/DCIM/VideoRecorder"
UPLOAD_SERVER="http://192.168.31.121:5000"
LOGS_FILE="/system/sdcard/log/send_record_image.log"

echo "Start recording Image"
RECORDING_PATH="$SAVE_DIR/$FILE"
/system/sdcard/bin/busybox nohup /system/sdcard/bin/getimage > "$RECORDING_PATH" && /system/sdcard/bin/curl --connect-timeout 10 -m 10 -F "file=@${RECORDING_PATH}" "$UPLOAD_SERVER" & >>"$LOGS_FILE" &