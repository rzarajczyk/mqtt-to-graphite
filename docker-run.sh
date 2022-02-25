#!/bin/bash
TMP=$(mktemp -d)
cp $(pwd)/config/* $TMP
echo "Temp directory is $TMP"
docker run -it --rm  \
    --add-host "graphite:192.168.86.159" \
    --add-host "mosquitto:192.168.86.159" \
    --name mqtt-to-graphite \
    -v $TMP:/mqtt-to-graphite/config \
    rzarajczyk/mqtt-to-graphite:latest
