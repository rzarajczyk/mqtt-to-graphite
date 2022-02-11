import logging
import os
import shutil
import socket
import time
from logging import config as logging_config

import paho.mqtt.client as mqtt
import yaml

ROOT = os.environ.get('APP_ROOT', ".")

########################################################################################################################
# logging configuration

LOGGER_CONFIGURATION = "%s/config/logging.yaml" % ROOT
if not os.path.isfile(LOGGER_CONFIGURATION):
    shutil.copy("%s/config-defaults/logging.yaml" % ROOT, LOGGER_CONFIGURATION)

with open(LOGGER_CONFIGURATION, 'r') as f:
    config = yaml.full_load(f)
    logging_config.dictConfig(config)

LOGGER = logging.getLogger("main")
LOGGER.info("Starting application!")

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
# utility functions

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_boolean(string):
    return string in ['true', 'false']


########################################################################################################################
# core logic

def is_acceptable(payload):
    return is_number(payload) or is_boolean(payload)


def normalize(payload):
    if payload == 'true':
        return 1
    elif payload == 'false':
        return 0
    else:
        return payload


def on_connect(client, userdata, flags, rc):
    LOGGER.info("Connected with result code %s" % str(rc))
    client.subscribe("homie/#")


def on_message(client, userdata, msg):
    payload = msg.payload.decode(encoding='UTF-8')
    parts = msg.topic.split('/')
    root = parts[0]
    if root == 'homie':
        i = 1
        while i < len(parts) and not parts[i].startswith("$"):
            i += 1
        if i == len(parts):
            path = '.'.join(parts[1:])
            if path not in IGNORE_PATHS:
                if is_acceptable(payload):
                    payload = normalize(payload)
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
