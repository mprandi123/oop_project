from telegram import Update
from telegram.ext import ContextTypes
from metaapi_cloud_sdk import MetaApi
from my_project.Utils import message_parser
import os
import logging


# MetaAPI Credentials
API_KEY = os.getenv("API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")


async def connect_metatrader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Attempts connection to MetaAPI and MetaTrader to place trade.
    https://pypi.org/project/metaapi-cloud-sdk/

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    # creates connection to MetaAPI
    api = MetaApi(token=API_KEY)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Trying to connect to MetaTrader (may it takes a few seconds)...\n",
    )

    try:
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        initial_state = account.state
        deployed_states = ["DEPLOYING", "DEPLOYED"]

        if initial_state not in deployed_states:
            #  wait until account is deployed and connected to broker
            logging.info("Deploying account")
            await account.deploy()

        logging.info("Waiting for API server to connect to broker ...")
        await account.wait_connected()

        # connect to MetaApi API
        connection = account.get_rpc_connection()
        await connection.connect()

        # wait until terminal state synchronized to the local state
        logging.info("Waiting for SDK to synchronize to terminal state ...")
        await connection.wait_synchronized()

        ###################################################################################################
        # ATTUALMENTE VARIABILE NON USATA
        ###################################################################################################
        # obtains account information from MetaTrader server (balance, margin, ecc ecc)
        account_information = await connection.get_account_information()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Successfully connected to MetaTrader!\n",
        )

    except Exception as error:
        logging.error(f"Error: {error}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There was an issue with the connection 😕\n\nError Message:\n{error}",
        )

    await message_parser(update=update, context=context,
                         connection=connection)


async def get_terminal_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TO IMPLEMENT
    return
