import paho.mqtt.client as mqtt
import csv, json
import telegram
import conf.conf as conf
import LogFile as clf
from pathlib import Path
import shutil, logging, re
import api_pushover, api_sms, api_mqtt

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=conf.loglevel)



def mqtt_on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def calculate_alarm(value,sensor):
    logging.info("Check if alarm")
    
    tmp_path = str(Path.cwd()).split('\'')[-1]+"/tmp"
    Path(tmp_path).mkdir(parents=True, exist_ok=True)
    
    filepath_hysteresis = clf.create_log_file(tmp_path,sensor,"hysterese")
    filepath_alarm      = clf.create_log_file(tmp_path,sensor,"alarm")

    logging.debug("Check:")
    if value <= conf.alarm_threshold_cap:
        logging.debug("" + str(value) + " <= " + str(conf.alarm_threshold_cap))

        hysteresis_was  = clf.FileContent(filepath_hysteresis)
        hysteresis_now  = hysteresis_was + 1
        clf.WriteData(filepath_hysteresis,hysteresis_now)
        
        if hysteresis_now >= conf.alarm_hysteresis:
            logging.debug("Hyteresenwert " + str(hysteresis_now) + " >= " + str(conf.alarm_hysteresis))
            
            alarm_was  = clf.FileContent(filepath_alarm)
            alarm_now   = alarm_was + 1
            
            if (alarm_now <= conf.alarm_resend) or (alarm_was == 0):
                clf.WriteData(filepath_alarm,alarm_now)
                logging.info("Alarm not known: Send alarm")
                return True
            else:
                logging.info("Alarm known: no alarm")
                return False
        else:
            logging.info("Hysteresis not reached: no alarm")
            return False
    else:
        logging.debug("" + str(value) + " > " + str(conf.alarm_threshold_cap))
        logging.info("Threshold not passed: no alarm")
        file_hysteresis = open(filepath_hysteresis,"w")
        file_hysteresis.write(str(0))
        file_alarm = open(filepath_alarm, "w")
        file_alarm.write(str(0))
        return False

# Managing multiple alarmoutputs while looking for messages on MQTT
def mqtt_on_message(mqttc, obj, msg):
    logging.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))   
    if "alarm" not in str(msg.topic) and re.compile(r'[0-9]*').search(str(msg.payload.decode("utf-8"))):
        sensor_location = str(msg.topic).split('/')[-1]
        if calculate_alarm(int(msg.payload.decode("utf-8")),sensor_location):        
            alarm_msg = "Ein Sensor in " + sensor_location + " meldet einen Alarm!"
            if conf.pushover_active:
                api_pushover.pushover_send(alarm_msg)
            if conf.telegram_active:
                bot.sendMessage(chat_id = conf.telegram_chat_id, text = alarm_msg)
            if conf.sms_activ:
                api_sms.sms_send(alarm_msg)
            if conf.mqtt_active:
                api_mqtt.mqtt_send(mqttc, alarm_msg,sensor_location)

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
if conf.mqtt_usetls:
    mqttc.tls_set(ca_certs = None, certfile = None, keyfile = None, cert_reqs = ssl.CERT_NONE, tls_version = ssl.PROTOCOL_TLSv1_2)

mqttc.username_pw_set(conf.mqtt_user, conf.mqtt_password)

mqttc.on_message = mqtt_on_message
mqttc.on_connect = mqtt_on_connect

tmp_path = Path(str(Path.cwd()).split('\'')[-1]+"/tmp")
shutil.rmtree(tmp_path)

logging.info("MQTT Connect" + conf.mqtt_host + " port: " + str(conf.mqtt_port))
mqttc.connect(conf.mqtt_host, conf.mqtt_port, 60)

for i in conf.mqtt_topics:
    mqttc.subscribe(i,0)
    logging.info("MQTT-Topic " + i + " subscribed")
    print("Subscribed to " + i)

if conf.telegram_active:
    bot = telegram.Bot(token = conf.telegram_token)
mqttc.loop_forever()
