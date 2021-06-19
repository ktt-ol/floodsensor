import paho.mqtt.client as mqtt
import logging
import http.client, urllib, ssl
import csv, json
import telegram
import conf

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

# Send a message thru Pushover
def pushover_send(message):
    logging.info("Pushover notification")
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
        "token":    conf.pushover_token,
        "user":     conf.pushover_user,
        "priority": conf.pushover_priority,
        "retry":    conf.pushover_retry,
        "expire":   conf.pushover_expire,
        "message":  message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# Send a message thru SMS
def sms_send(message):
    logging.info("SMS notification")
    conn    = http.client.HTTPSConnection("gateway.sms77.io")
    headers = {'Content-type': 'application/json'}
    with open('numbers.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            foo         = {"p": conf.sms_key, "to": row['phonenumber'], "text": message, "from": "Mainframe"}
            json_foo    = json.dumps(foo)
            conn.request('POST', '/api/sms', json_foo, headers)
            response    = conn.getresponse()


def mqtt_on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

# Determin weather the message is suitable for triggering an alarm
def mqtt_on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print(msg.payload.decode("utf-8"))
    y = "Ein Sensor in " + str(msg.topic).split('/')[-1] + " meldet einen Alarm!"
    if msg.payload.decode("utf-8") == "True":
        pushover_send(y)
        bot.sendMessage(chat_id = conf.telegram_chat_id, text = y)
        sms_send(y)

# Log MQTT to Terminal and Log-File
def mqtt_on_log(mqttc, obj, level, string):
    logging.info("MQTT-LOG: " + string)
    print(string)
    
if conf.mqtt_port is None:
    if conf.mqtt_usetls:
        conf.mqtt_port = 8883
    else:
        conf.mqtt_port = 1883
        
mqttc = mqtt.Client(conf.mqtt_clientid, clean_session = conf.mqtt_clean_session)
mqttc.tls_set(ca_certs = None, certfile = None, keyfile = None, cert_reqs = ssl.CERT_NONE, tls_version = ssl.PROTOCOL_TLSv1_2)
mqttc.username_pw_set(conf.mqtt_user, conf.mqtt_password)


mqttc.on_message = mqtt_on_message
mqttc.on_connect = mqtt_on_connect

logging.info("MQTT Connect" + conf.mqtt_host + " port: " + str(conf.mqtt_port))
print("Connecting to " + conf.mqtt_host + " port: " + str(conf.mqtt_port))
mqttc.connect(conf.mqtt_host, conf.mqtt_port, 60)

for i in conf.mqtt_topics:
    mqttc.subscribe(i,0)
    logging.info("MQTT-Topic " + i + " subscribed")
    print("Subscribed to " + i)

bot = telegram.Bot(token = conf.telegram_token)
mqttc.loop_forever()

