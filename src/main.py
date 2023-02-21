import socket
import time

import paho.mqtt.client as mqtt
from apscheduler.schedulers.background import BackgroundScheduler
from bootstrap.bootstrap import start_service

config, logger, timezone = start_service()

GRAPHITE_HOST = config['graphite']['host']
GRAPHITE_PORT = config['graphite']['port']
MQTT_HOST = config['mqtt']['host']
MQTT_PORT = config['mqtt']['port']
MQTT_USER = config['mqtt']['user']
MQTT_PASS = config['mqtt']['password']
CONVERTIONS = config['convertions']


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code %s" % str(rc))
    client.subscribe("homie/#")


def convert(topic, payload):
    if is_number(payload):
        return payload
    if payload == 'true':
        return 1
    if payload == 'false':
        return 0
    if topic in CONVERTIONS:
        return CONVERTIONS[topic].get(payload, None)
    else:
        return None


METRICS = {}


def on_message(client, userdata, msg):
    topic: str = msg.topic
    payload = msg.payload.decode(encoding='UTF-8')
    if topic.startswith('homie/'):
        if not topic.endswith('/set'):
            if '$' not in topic:
                path = topic.replace('/', '.')
                converted_payload = convert(topic, payload)
                if converted_payload is not None:
                    METRICS[path] = converted_payload
                    logger.debug('> metric received: %s -> %s' % (topic, converted_payload))
                else:
                    logger.warning('> IGNORING: %s -> %s' % (topic, payload))


def run():
    logger.info("Sending metrics...")
    now = int(time.time())
    sock = socket.socket()
    sock.connect((GRAPHITE_HOST, GRAPHITE_PORT))
    for path in METRICS:
        metric = '%s %s %d\n' % (path, METRICS[path], now)
        logger.info('> sending: %s' % metric.strip())
        sock.sendall(metric.encode(encoding='UTF-8'))
    sock.close()
    logger.info("Sending metrics finished")


client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT)

scheduler = BackgroundScheduler(timezone=timezone)
scheduler.add_job(run, 'interval', seconds=10)
scheduler.start()

client.loop_forever()
