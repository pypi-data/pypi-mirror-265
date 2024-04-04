import time
import uuid

import paho.mqtt.client as mqtt_client

from elf_py_utils import elf_core, str_util

logger = elf_core.set_logging('MqttUtil')
config = elf_core.get_config()

MQTT_ERR_SUCCESS = mqtt_client.MQTT_ERR_SUCCESS
MQTT_ERR_NO_CONN = mqtt_client.MQTT_ERR_NO_CONN
MQTT_ERR_QUEUE_SIZE = mqtt_client.MQTT_ERR_QUEUE_SIZE


class MqttClient:

    def __init__(self):
        self.client_id = f'python-mqtt-{uuid.uuid1().hex}'
        self.host = str(config.read_config('mqtt.host'))
        self.port = str(config.read_config('mqtt.port'))
        self.user = str(config.read_config('mqtt.user'))
        self.password = str(config.read_config('mqtt.password'))
        self.client = mqtt_client.Client(self.client_id)

    def connect_mqtt(self):
        if str_util.is_blank(self.host) or str_util.is_blank(self.port):
            logger.error('You must specify a host')

        try:
            logger.info('Try to connect host {} port {} '.format(self.host, self.port))
            if str_util.is_not_blank(self.user) or str_util.is_not_blank(self.password):
                self.client.username_pw_set(self.user, self.password)
            self.client.connect_async(self.host, int(self.port))
            self.client.loop_start()
            self.wait_for_connected(self.client)
        except Exception as e:
            logger.warning('Connect to MQTT Failed!')

    def on_disconnect(self, rc):
        logger.warning("Disconnected result code %s", rc)
        self.connect_mqtt()

    def on_connect(self, rc):
        if rc == 0:
            logger.info('Connected to MQTT Success, Host:%s, Port:%s', self.host, self.port)
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    @staticmethod
    def wait_for_connected(client, time_out=5):
        count = 0
        logger.info("Connecting...... {} S  {}".format(count, client))
        while (not client.is_connected()) and (count < time_out):
            count += 1
            time.sleep(1)
            logger.info("Connecting...... %dS", count)
