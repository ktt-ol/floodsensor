import paho.mqtt.client as mqtt
import credentials
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))
    client.subscribe("/test/01")

def on_message(client, userdata, msg):
    logging.info(msg.topic+" "+str(msg.payload))

def connect_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(credentials.mqtt_user,credentials.mqtt_pass)
    client.connect(credentials.mqtt_host, credentials.mqtt_port, 60)
    client.loop_forever()