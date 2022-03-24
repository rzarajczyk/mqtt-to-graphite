# mqtt-to-graphite

Exports metrics from MQTT Homie convention to Graphite.

`mqtt-to-graphite` subscribes to every MQTT sub-topics of the `homie/` root (`homie/#`), except:

* the ones ending with `/set` (these have a special meaning in the Homie Convention)
* the ones containing `$` in the topic path (these have also a special meaning in the Homie Convention)

Once subscribed, it listens to every value and:

* if the value is a valid number, it will export it as Graphite metric
* if the value is a string `true` or `false`, it will export it as Graphite metric, with values mapped to `1`/`0`
* if the topic and value are specified in the `mqtt-to-graphite.yaml` configuration file, it will export it as Graphite
  metric using mapping from the configuration

The Graphite metric path will be constructed from the MQTT path.

**Note**: `mqtt-to-graphite` does not support any kind of structured values, like JSON, YAML etc.

### Important notice: metrics are sent every 10 seconds

The `mqtt-to-graphite` collects all metrics in the intermediate buffer, and sends the whole buffer to Graphite every 10
seconds. This behavior means have several implications:

1.) The Graphite charts are always connected lines, without any "holes"

The Graphite charts are always connected lines, even if displaying metrics older than 6 hours.

The default configuration of the official Docker image of Graphite is constructed in the way, that if the metric is sent
less frequently then once per 10 seconds, the Graphite will now show it after 6 hours.

2.) All the metrics live forever

Even if the last message in the topic was ages ago, it will still be exported every 10 seconds - and the chart will just
show horizontal line.

The only way to completely stop sending metric is to delete MQTT topic.

3.) It may drop some frequently changing values

If the values in some topic changes more frequently then once per 10 seconds, only some of its values will be sent to
Graphite

## Usage in `docker-compose.yaml`

```dockerfile
version: '3.2'
services:
  mqtt-to-graphite:
    image: rzarajczyk/mqtt-to-graphite:latest
    volumes:
      - ./config/mqtt-to-graphite.yaml:/mqtt-to-graphite/config/mqtt-to-graphite.yaml
    restart: unless-stopped
    network_mode: host
```

## Required configuration

The file `mqtt-to-graphite.yaml` should contain the following:

```yaml
graphite:
  host: <<graphite hostname/ip>>
  port: <<graphite port>>

mqtt:
  host: <<mqtt hostname/ip>>
  port: <<mqtt port>>
  user: <<mqtt username>>
  password: <<mqtt password>>

convertions:
  "homie/some/topic/path/for/example/purifier/speed":
    "off": 0
    "silent": 0.5
    "1": 1
    "2": 2
    "3": 3
    "4": 4
    "5": 5
    "6": 6
    "7": 7
    "8": 8
    "9": 9
    "10": 10
    "11": 11
    "12": 12
    "13": 13
    "14": 14
    "15": 15
    "16": 16
    "auto": -1
  "some/other/topic/for/example/power-status":
    "active": 1
    "standby": 0
    "off": -1
```

The `graphite` ans `mqtt` parts should be self-explaining

The `convertions` contains the list of topics as sub-keys, each of them contains the mapping of possible value to some
number. If the mapping for the received topic and value exists in the configuration, it will be used to send appropriate
metric.

### Hardcoded important values

* the metrics are sent every **10 seconds**
* the metrics use timestamps generated with assumption of the timezone: **Europe/Warsaw**