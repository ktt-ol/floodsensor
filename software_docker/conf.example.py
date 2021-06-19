#MQTT
mqtt_host = ""  # Hostname or IP from MQTT Broker
mqtt_port = None            # MQTT Broker Port -> None if Standard Ports (SSL 8883, no SSL 1883)
mqtt_usetls = True          # Use TLS or not?
mqtt_clientid = ""  # Provide Client-ID
mqtt_user = ""          # MQTT Username
mqtt_password = ""      # MQTT Password
mqtt_clean_session = True   # Clean-Session?
mqtt_topics = [""] # Array of all Topics that should Subscribed

#Telegram-Bot
telegram_token = ""
telegram_chat_id = ""

#Pushover
pushover_token = ""
pushover_user = ""
pushover_title = ""
pushover_priority = 1
pushover_retry = 30
pushover_expire = 120

#sms77.io
sms_key = ""
