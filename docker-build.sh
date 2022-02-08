#!/bin/bash
TAG=$1
if [ -z $TAG ]; then
    echo "TAG is required"
    exit 1
fi

docker build -t rzarajczyk/mqtt-to-graphite:$TAG .
docker tag rzarajczyk/mqtt-to-graphite:$TAG rzarajczyk/mqtt-to-graphite:latest
