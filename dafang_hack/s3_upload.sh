#!/usr/bin/env bash

FILE=$1
DIR_NAME="/home/pi/.homeassistant/www/snapshot"
FILE_PATH="$DIR_NAME/$FILE"
BUCKET_NAME="dafang"
S3_SUB_DIR="$(date +%Y%m%d)"
NEW_NAME="$S3_SUB_DIR/$FILE"
echo $NEW_NAME
echo $FILE_PATH

/home/pi/cli-ve/bin/aws s3 cp "$FILE_PATH" "s3://$BUCKET_NAME/$NEW_NAME"