#!/bin/bash

/usr/bin/flock -w 0 /var/run/192.168.$1.100.lock /home/mac/proxyHobbit/reconnect.sh -r 4G  -i 192.168.$1.1 /etc/init.d/3proxy start192.168.$1.1 >/dev/null 2>&1