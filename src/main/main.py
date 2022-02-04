import socket

import paho.mqtt.client as mqtt
import time
import logging
import os
import shutil
import yaml
from logging import config as logging_config


ROOT = "/mqtt-to-graphite"

########################################################################################################################
# logging configuration

LOGGER_CONFIGURATION = "%s/config/logging.yaml" % ROOT
if not os.path.isfile(LOGGER_CONFIGURATION):
    shutil.copy("%s/config-defaults/logging.yaml" % ROOT, LOGGER_CONFIGURATION)

with open(LOGGER_CONFIGURATION, 'r') as f:
    config = yaml.full_load(f)
    logging_config.dictConfig(config)

LOGGER = logging.getLogger("main")

########################################################################################################################
# application configuration

CONFIGURATION = "%s/config/application.yaml" % ROOT
if not os.path.isfile(CONFIGURATION):
    shutil.copy("%s/config-defaults/application.yaml" % ROOT, CONFIGURATION)

with open(CONFIGURATION, 'r') as f:
    config = yaml.full_load(f)

    GRAPHITE_HOST = config['graphite']['host']
    GRAPHITE_PORT = config['graphite']['port']
    MQTT_HOST = config['mqtt']['host']
    MQTT_PORT = config['mqtt']['port']
    MQTT_USER = config['mqtt']['user']
    MQTT_PASS = config['mqtt']['password']

    IGNORE_PATHS = config['ignore']['paths']

########################################################################################################################
# utility finctions

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

########################################################################################################################
# core logic

def on_connect(client, userdata, flags, rc):
    LOGGER.info("Connected with result code %s" % str(rc))
    client.subscribe("homie/#")


def on_message(client, userdata, msg):
    payload = msg.payload.decode(encoding='UTF-8')
    if is_number(payload):
        parts = msg.topic.split('/')
        root = parts[0]
        if root != 'homie':
            LOGGER.warning('unsupported topic: %s (root is not "homie")' % msg.topic)
        i = 1
        while i < len(parts) and not parts[i].startswith("$"):
            i += 1
        if i == len(parts):
            path = '.'.join(parts[1:])
            if path not in IGNORE_PATHS:
                metric = '%s %s %d\n' % (path, payload, int(time.time()))
                LOGGER.info('> sending: %s' % metric.strip())
                sock = socket.socket()
                sock.connect((GRAPHITE_HOST, GRAPHITE_PORT))
                sock.sendall(metric.encode(encoding='UTF-8'))
                sock.close()


client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT)

client.loop_forever()
