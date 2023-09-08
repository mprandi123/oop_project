from My_project.StartHelpCommand import *
from My_project.Connection import connect_metatrader
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
import os


# Telegram Credentials
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def main() -> None:
    """Runs the Telegram bot."""

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # To tell your bot to listen to /start commands, you can use a CommandHandler (one of the provided Handler subclasses) and register it in the application
    welcome_handler = CommandHandler("start", welcome)
    application.add_handler(welcome_handler)

    help_handler = CommandHandler("help", help)
    application.add_handler(help_handler)

    connection_handler = MessageHandler(filters.TEXT, connect_metatrader)
    application.add_handler(connection_handler)

    # Every 60 seconds ask Telegram server if there is any new messages
    application.run_polling()


if __name__ == "__main__":
    main()
