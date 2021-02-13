import csv
import base64

from telegram import Update
from telegram.ext import CallbackContext, MessageFilter
from datetime import datetime
from io import StringIO

class PressureMeasureRecord:
    def __init__(self, timestamp, diastolic, systolic, pulse):
        self.date = datetime.fromtimestamp(timestamp)
        self.diastolic = diastolic
        self.systolic = systolic
        self.pulse = pulse

class PressureReportFilter(MessageFilter):
    def filter(self, message):
        msg_text = message.text.lower()
        return msg_text.find("отчет") != -1 and msg_text.find("давлени") != -1

class PressureReportHandler:
    def __init__ (self, db_connection, logger):
        self.db_connection = db_connection
        self.logger = logger
    
    def get_filter(self):
        return PressureReportFilter()

    def handle(self, update: Update, context: CallbackContext) -> None:
        self.logger.info("Executing pressure report handler ...")
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ts, systolic, diastolic, pulse FROM pressure_measures WHERE user_id=" + str(update.message.from_user.id))
        rows = cursor.fetchall()

        f = StringIO()
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["timestamp", "systolic", "diastolic", "pulse"])
        for row in rows:
            (timestamp, systolic, diastolic, pulse) = row
            writer.writerow([timestamp, systolic, diastolic, pulse])
        f.seek(0)

        context.bot.send_document(chat_id=update.effective_chat.id, document=f, filename="давление.csv")

        self.logger.info(f"Pressure report handler executed")
