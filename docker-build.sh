#!/bin/bash
TAG=$(date '+%Y%m%d')
docker build -t rzarajczyk/mqtt-to-graphite:$TAG .
docker tag rzarajczyk/mqtt-to-graphite:$TAG rzarajczyk/mqtt-to-graphite:latest
docker push rzarajczyk/mqtt-to-graphite:$TAG
docker push rzarajczyk/mqtt-to-graphite:latest
