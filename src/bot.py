import logging
import sys
import os
import sqlite3
import configparser

from ErrorHandler import ErrorHandler
from PressureHandler import PressureHandler
from PressureReportHandler import PressureReportHandler

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, MessageFilter
        
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("Assistant bot")

if len(sys.argv) != 2:
    print("Usage: bot.py pathToConfig")
    exit(1)

path_to_settings = sys.argv[1]
config = configparser.ConfigParser()
config.read(path_to_settings)

db_file_name = config["database"]["db_file_name"]
db_connection = sqlite3.connect(db_file_name, check_same_thread=False)

tg_apikey = config["telegram"]["api_key"]
updater = Updater(tg_apikey, use_context=True)

pressure_handler = PressureHandler(db_connection, logger)
updater.dispatcher.add_handler(MessageHandler(pressure_handler.get_filter(), pressure_handler.handle))

pressure_report_handler = PressureReportHandler(db_connection, logger)
updater.dispatcher.add_handler(MessageHandler(pressure_report_handler.get_filter(), pressure_report_handler.handle))

error_handler = ErrorHandler(logger)
updater.dispatcher.add_error_handler(error_handler.handle)

updater.start_polling()
updater.idle()

db_connection.close()