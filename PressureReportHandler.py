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
        return "отчет давление"

class PressureReportHandler:
    def __init__ (self, db_connection, logger):
        self.db_connection = db_connection
        self.logger = logger
    
    def get_filter(self):
        return PressureReportFilter()

    def handle(self, update: Update, context: CallbackContext) -> None:
        self.logger.info("Executing pressure report handler ...")
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM pressure_measures")
        rows = cursor.fetchall()

        f = StringIO()
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["timestamp", "systolic", "diastolic", "pulse"])
        for row in rows:
            (timestamp, systolic, diastolic, pulse) = row
            date = datetime.fromtimestamp(timestamp).isoformat(timespec="seconds")
            writer.writerow([date, systolic, diastolic, pulse])
        f.seek(0)

        context.bot.send_document(chat_id=update.effective_chat.id, document=f, filename="давление.csv")

        self.logger.info(f"Pressure report handler executed")
