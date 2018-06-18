#!/bin/sh

PIDFILE="/run/send_record_video.pid"
FILE=`date +%Y%m%d%H%M%S.mp4`

pid_exists () {
    # This is better than "kill -0" because it doesn't require permission to
    # send a signal (so daemon_status in particular works as non-root).
    test -d /proc/"$1"
}
echo "start" >> /system/sdcard/log/sen_send_record_video.log
pid="$(cat "$PIDFILE" 2>/dev/null)"
if [ "$pid" ] && pid_exists "${pid}"; then
  echo "send_record_video now run ${pid}" >> /system/sdcard/log/sen_send_record_video.log
else
  /system/sdcard/bin/busybox nohup /system/sdcard/bin/avconv -rtsp_transport tcp -y -i rtsp://0.0.0.0:8554/unicast -vcodec copy -c:a aac -strict experimental -t 15 /system/sdcard/DCIM/VideoRecorder/$FILE && /system/sdcard/bin/curl --connect-timeout 10 -m 20 -F "file=@/system/sdcard/DCIM/VideoRecorder/${FILE}" http://192.168.31.121:5000 &

  echo "$!" > "$PIDFILE"
fi