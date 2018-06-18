#!/bin/sh

PIDFILE="/run/send_record_video.pid"
FILE=`date +%Y%m%d%H%M%S.mp4`
SAVE_DIR="/system/sdcard/DCIM/VideoRecorder"
UPLOAD_SERVER="http://192.168.31.121:5000"

pid_exists () {
    # This is better than "kill -0" because it doesn't require permission to
    # send a signal (so daemon_status in particular works as non-root).
    test -d /proc/"$1"
}

status()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
    kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
  fi
}

start()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ -f $PIDFILE ] && pid_exists "${pid}"; then
    echo "send_record_video now run ${pid}" >> /system/sdcard/log/sen_send_record_video.log
#    echo "send_record_video now run ${pid}"
  else
    echo "Start recording"
    RECORDING_PATH="$SAVE_DIR/$FILE"
    echo "$RECORDING_PATH"
    /system/sdcard/bin/busybox nohup /system/sdcard/bin/avconv -rtsp_transport tcp -y -i rtsp://0.0.0.0:8554/unicast -vcodec copy -c:a aac -strict experimental -t 15 "$RECORDING_PATH" && /system/sdcard/bin/curl --connect-timeout 10 -m 20 -F "file=@${RECORDING_PATH}" "$UPLOAD_SERVER" &>/dev/null &
    echo "$!" > "$PIDFILE"
  fi
}

stop()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
    kill "$pid" &&  rm "$PIDFILE"
    echo "Stopped recording"
  else
    echo "Could not find a running recording to stop."
  fi
}

if [ $# -eq 0 ]; then
  start
else
  case $1 in start|stop|status)
      $1
      ;;
  esac
fi