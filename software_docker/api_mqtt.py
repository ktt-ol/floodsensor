import logging, conf

def mqtt_send(mqttc, message,sensor):
    logging.info("MQTT notification")
    mqttc.publish(conf.mqtt_topic_prefix + "/" + sensor + "/alarm", payload=message, retain=True)