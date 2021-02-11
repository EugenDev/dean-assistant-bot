import logging
import os
import sqlite3

from settings import TgConnectionSettings

from ErrorHandler import ErrorHandler
from PressureHandler import PressureHandler
from PressureReportHandler import PressureReportHandler

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, MessageFilter
        
def create_tables(db_connection):
    with open(r'..\create_tables.sql', 'r') as content_file:
        init_script_lines =  content_file.readlines()
        for line in init_script_lines:
            db_connection.execute(line)

def get_settings():
    result = {}
    with open(r'..\.env', 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.split("=")
            result[key] = value
    return result

def main(settings, logger):
    db_connection = sqlite3.connect("assistant.db", check_same_thread=False)
    create_tables(db_connection)

    tg_apikey = settings["tg_apikey"]
    updater = Updater(tg_apikey, use_context=True)

    dispatcher = updater.dispatcher    

    pressure_handler = PressureHandler(db_connection, logger)
    dispatcher.add_handler(MessageHandler(pressure_handler.get_filter(), pressure_handler.handle))

    pressure_report_handler = PressureReportHandler(db_connection, logger)
    dispatcher.add_handler(MessageHandler(pressure_report_handler.get_filter(), pressure_report_handler.handle))

    error_handler = ErrorHandler(logger)
    dispatcher.add_error_handler(error_handler.handle)

    updater.start_polling()
    updater.idle()

    db_connection.close()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("Assistant bot")

settings = get_settings()
main(settings, logger)
