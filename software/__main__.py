from telegram.bot import log
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
import logging, getmqtt
import language.select as ls
import multiprocessing as mp
print("Number of processors: ", mp.cpu_count())

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

    
ls.language("de_DE")

def start(lang, update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=lang.msg_info_fist_hello)

def unknown(lang, update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=lang.msg_info_not_a_command)

def send_alarm(lang, update, context):
    logging.debug("SEND ALARM")
    sensor = 0x01
    value = 0.00
    context.bot.send_message(chat_id=update.effective_chat.id, text=lang.msg_alarm_info + sensor +" | " + value)
    
updater         = Updater(token='1816627937:AAG5bPafYf587tfvtfmRgPhAPUjEag0ZgGU', use_context=True)
dispatcher      = updater.dispatcher

start_handler   = CommandHandler('start', start)
alarm_handler   = MessageHandler(Filters.text & Filters.regex('test'), send_alarm)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(alarm_handler)
dispatcher.add_handler(unknown_handler)

logging.debug("Polling start")

end_loop = False
while not end_loop:
        mqtt = getmqtt.connect_mqtt()
        telegram = updater.start_polling()