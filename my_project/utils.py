from telegram import Update
from telegram.ext import ContextTypes
import regex as re


async def message_parser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> dict:
    """message parser to extract order info from update object

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks

    Returns:
        dict: currency pair, order type, opening price, stop loss, take profit
    """
    message = update.message  # Ottieni l'oggetto Message dall'aggiornamento
    text = message.text  # Ottieni il testo del messaggio

    order_info = {}

    # Estraggo la coppia di valute
    CurrencyPair = re.search(r"(\w+)/(\w+)", text)
    if CurrencyPair:
        # va bene anche solo CurrencyPair.group()
        order_info["CurrencyPair"] = f"{CurrencyPair.group(1)}{CurrencyPair.group(2)}"

    # Estraggo il tipo di ordine (buy o sell)
    OrderType = re.search(
        r"(buy|sell)( limit| stop| diretta a mercato)", text, re.IGNORECASE
    )
    if OrderType:
        order_info["OrderType"] = OrderType.group().lower()

    # Estraggo il prezzo di apertura
    OpeningPrice = re.search(r"Prezzo\s+(\d+\.\d+)", text)
    if OpeningPrice:
        order_info["OpeningPrice"] = float(OpeningPrice.group(1))

    # Estraggo il prezzo di Stop Loss
    StopLoss = re.search(r"stop\s+loss.*?(\d+\.\d+)", text, re.IGNORECASE)
    if StopLoss:
        order_info["StopLoss"] = float(StopLoss.group(1))

    # Estraggo il prezzo di Take Profit
    TakeProfit = re.search(r"take\s+profit.*?(\d+\.\d+)", text, re.IGNORECASE)
    if TakeProfit:
        order_info["TakeProfit"] = float(TakeProfit.group(1))

    # Per debug
    await context.bot.send_message(chat_id=update.effective_chat.id, text=order_info)

    return order_info
