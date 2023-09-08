from telegram import Update
from telegram.ext import ContextTypes


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends welcome message to user.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    welcome_message = """Welcome to this bot developed by mprandi.
    \nThe aim is receiving orders from TRFX channel and place them in MT4 or MT5.
    \nPlease send me the orders!"""

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=welcome_message
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends help message to user.

    Arguments:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks
    """

    help_message = """Svegliati e mandami tutte le info per inviare un ordine a mercato:
    \n- Currency pair: cfd che vuoi tradare;
    \n- Tipo ordine: buy/sell limit, buy/sell stop, buy/sell diretta a mercato;
    \n- Prezzo di apertura: utilizza il '.' e non la ',' ;
    \n- Stop loss;
    \n- Take profit;"""

    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)
