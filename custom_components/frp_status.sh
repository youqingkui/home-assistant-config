#!/usr/bin/env bash

pid=`ps aux |grep frpc | grep -v grep | awk '{print $2}'`
if [ "$pid" ]; then
	echo "ok"
else
	echo "not"
fi
