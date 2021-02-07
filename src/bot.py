import logging
import os
import psycopg2

from settings import TgConnectionSettings, DbSettings

from PressureHandler import PressureHandler
from PressureReportHandler import PressureReportHandler

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, MessageFilter
        
def main(tgSettings: TgConnectionSettings, dbSettings: DbSettings, logger):
    print(dbSettings.database, dbSettings.user, dbSettings.password, dbSettings.host, dbSettings.port)
    db_connection = psycopg2.connect(database=dbSettings.database, user=dbSettings.user, password=dbSettings.password, host=dbSettings.host, port=dbSettings.port)
    cursor = db_connection.cursor()
    with open('create_tables.sql', 'r') as content_file:
        init_script_lines =  content_file.readlines()
        for line in init_script_lines:
            cursor.execute(line)

    updater = Updater(tgSettings.api_key, use_context=True)

    dispatcher = updater.dispatcher    

    pressure_handler = PressureHandler(db_connection, logger)
    dispatcher.add_handler(MessageHandler(pressure_handler.get_filter(), pressure_handler.handle))

    pressure_report_handler = PressureReportHandler(db_connection, logger)
    dispatcher.add_handler(MessageHandler(pressure_report_handler.get_filter(), pressure_report_handler.handle))

    updater.start_polling()
    updater.idle()

    db_connection.close()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("Assistant bot")

dbSettings = DbSettings(os.environ["pg_database"], os.environ["pg_user"], os.environ["pg_password"], os.environ["pg_host"], os.environ["pg_port"])
tgConnectionSettings = TgConnectionSettings(os.environ["tg_api_key"])

main(tgConnectionSettings, dbSettings, logger)
