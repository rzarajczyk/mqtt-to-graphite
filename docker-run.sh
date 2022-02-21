#!/bin/bash
docker run -it --rm  \
    --name mqtt-to-graphite \
    -v $(pwd)/config:/mqtt-to-graphite/config \
    -v $(pwd)/logs:/mqtt-to-graphite/logs \
    rzarajczyk/mqtt-to-graphite:latest
