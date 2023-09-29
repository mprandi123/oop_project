from my_project.helpStopCommand import *
from my_project.connection import connect_metatrader
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import logging
import os

# Telegram Credentials
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# https://realpython.com/lessons/logging-python-introduction/
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Exceptions%2C-Warnings-and-Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Runs the Telegram bot.
    https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions---Your-first-Bot
    """

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # To tell your bot to listen to /help commands, you can use a CommandHandler (one of the provided Handler subclasses) and register it in the application
    help_handler = CommandHandler("help", help)
    application.add_handler(help_handler)

    stop_handler = CommandHandler("stop", system_stop)
    application.add_handler(stop_handler, )

    connect_handler = MessageHandler(filters.TEXT, connect_metatrader)
    application.add_handler(connect_handler)

    # Every 10 seconds ask Telegram server if there is any new messages
    application.run_polling()


if __name__ == "__main__":
    main()
