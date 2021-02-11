from telegram import Update
from telegram.ext import CallbackContext

class ErrorHandler:
    def __init__(self, logger):
        self.logger = logger

    def handle(self, update: Update, context: CallbackContext):
        update.message.reply_text("Произошла ошибка")
        self.logger.error(context.error)