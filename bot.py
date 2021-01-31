import logging
import os
import sqlite3

from PressureHandler import PressureHandler
from PressureReportHandler import PressureReportHandler

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, MessageFilter
        
def main(api_key):
    db_connection = sqlite3.connect("assistant.db", check_same_thread=False)

    with open('create_tables.sql', 'r') as content_file:
        init_script_lines =  content_file.readlines()
        for line in init_script_lines:
            db_connection.execute(line)

    updater = Updater(api_key, use_context=True)

    dispatcher = updater.dispatcher    

    pressure_handler = PressureHandler(db_connection, logger)
    dispatcher.add_handler(MessageHandler(pressure_handler.get_filter(), pressure_handler.handle))

    pressure_report_handler = PressureReportHandler(db_connection, logger)
    dispatcher.add_handler(MessageHandler(pressure_report_handler.get_filter(), pressure_report_handler.handle))

    updater.start_polling()
    updater.idle()

    db_connection.close()

print("Starting bot...")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("Assistant bot")

items_list = []

api_key = os.environ["tg_api_key"]
main(api_key)
