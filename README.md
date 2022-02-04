# mqtt-to-graphite

Exports metrics from MQTT (sent by Athom Homey in Homie convention) to Graphite

## Not recommended to general usage!
This code is written mainly for my personal purpose. I do not take any responsibility for this code,
and I will not provide any support for it. If you really want to use it - ok, but make sure you know
what you're doing.

### Usage
Build:
```shell
docker build -t rzarajczyk/mqtt-to-graphite:<<newtag>> .
docker tag rzarajczyk/mqtt-to-graphite:<<newtag>> rzarajczyk/mqtt-to-graphite:latest
```
Run:
```shell
docker run -it --rm  --network="host" --name mqtt-to-graphite -v $(pwd)/config:/mqtt-to-graphite/config -v $(pwd)/logs:/mqtt-to-graphite/logs rzarajczyk/mqtt-to-graphite:latest
```
Directories to mount:
 - `/mqtt-to-graphite/config` - it will contain config file. If directory is empty, sample config will be created.
 - `/mqtt-to-graphite/logs` - it will contain log file.
