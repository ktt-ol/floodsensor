###########################################################################
#MQTT

# Activate MQTT alarm messages
mqtt_active         = True
# Hostname or ip from the mqtt-broker
mqtt_host           = "10.10.10.10"
# MQTT broker port -> None if standard ports (SSL 8883, no SSL 1883)
mqtt_port           = 1883
# Use TLS or not?
mqtt_usetls         = False
# Provide Client-ID
mqtt_clientid       = "somerdmstring"
# MQTT username
mqtt_user           = "username"
# MQTT password
mqtt_password       = "password"
# Clean-session?
mqtt_clean_session  = True
# Array of all topics that should subscribed
mqtt_topics         = ["/test/testloc/#"]
# Prefix of the Topic to write to (/+/alarm etc.)
mqtt_topic_prefix   = "/test/testloc"

############################################################################
#Telegram-Bot

# Activate Telegram as a notification service
telegram_active     = False
# API-Token
telegram_token      = ""
# Telegram Chat ID (eather single user or group)
telegram_chat_id    = ""

###########################################################################
#Pushover

# Activate Pushover for messages
pushover_active     = True
# API-Token
pushover_token      = "APi_TOKEN_HERE"
# API-Username
pushover_user       = "EMAIL HERE"
# Title for the message
pushover_title      = "This is a Test"
# Priority
pushover_priority   = 1
# Retry interval (sec)
pushover_retry      = 30
# Retry until this time interval (sec)
pushover_expire     = 120

###########################################################################
# sms77.io

# Activate SMS-Messageing
sms_activ           = False
# SMS77.io API-Key
sms_key             = ""

###########################################################################
# Alarming

# Analog threshold where a alarm should be send (Lower -> More Water)
alarm_threshold_cap = 800
# How often a sensor has to be beneath the threshold to trigger an alarm
alarm_hyteresis     = 2
# Number of times a alarm should be resend, after the hysteresis is overflown
alarm_resend        = 1

###########################################################################