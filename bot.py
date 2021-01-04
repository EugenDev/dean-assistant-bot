import logging
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, MessageFilter

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class PressureFilter(MessageFilter):
    def filter(self, message):
        return 'давление' in message.text.lower()

def pressure_handler(update: Update, context: CallbackContext) -> None:
    logger.info("Received:" + update.message.text)
    update.message.reply_text(update.message.text)

def main(api_key):
    updater = Updater(api_key, use_context=True)

    dispatcher = updater.dispatcher    
    pressure_filter = PressureFilter()
    dispatcher.add_handler(MessageHandler(pressure_filter, pressure_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main(os.environ["tg_api_key"])