from telegram import Update
from telegram.ext import ContextTypes
import sys

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends help message to user.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    help_message = """ Welcome to this bot developed by mprandi.
    \nThe aim is receiving orders from TRFX channel and place them in MT4.
    \nPlease send me the orders!
    \n- Currency pair: CFD that you want to trade;
    \n- Order type: buy/sell limit, buy/sell stop, buy/sell direct to market;
    \n- Open price: use the '.' not the ',' ;
    \n- Stop loss;
    \n- Take profit;"""

    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

    return


async def system_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stops the connection, the polling and the system.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
        connection (_type_): istance from account.get_rpc_connection() to connect with MetaApi;
    """

    stop_message = "Program stopped."

    #await connection.close()
    #application.run_polling(stop_signals=True)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=stop_message)

    sys.exit()
