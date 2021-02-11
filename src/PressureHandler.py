from telegram import Update
from telegram.ext import CallbackContext, MessageFilter
from datetime import datetime

class PressureFilter(MessageFilter):
    def filter(self, message):
        return message.text.lower().startswith("давление")

class PressureHandler:
    def __init__ (self, db_connection, logger):
        self.db_connection = db_connection
        self.logger = logger
    
    def get_filter(self):
        return PressureFilter()

    def handle(self, update: Update, context: CallbackContext) -> None:
        self.logger.info("Executing pressure handler ...")
        splited_string = update.message.text.split()
        (systolic, diastolic, pulse) = splited_string[1:]
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO pressure_measures VALUES (?, ?, ?, ?)", (datetime.utcnow(), systolic, diastolic, pulse))
        self.db_connection.commit()
        update.message.reply_text(f"Добавлена запись в журнал давления: {systolic}, {diastolic}, {pulse}")
        self.logger.info(f"Pressure handler executed: {systolic}, {diastolic}, {pulse}")
