#!/bin/bash
TMP=$(mktemp -d)
cp $(pwd)/config/* $TMP
echo "Temp directory is $TMP"
docker run -it --rm  \
    --name mqtt-to-graphite \
    -v $TMP:/mqtt-to-graphite/config \
    rzarajczyk/mqtt-to-graphite:latest
