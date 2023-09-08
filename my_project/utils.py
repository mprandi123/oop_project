from telegram import Update
from telegram.ext import ContextTypes
from My_project.TradeClass import Trade
import regex as re


async def message_parser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """message parser to extract order info from update object

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks

    """
    message = update.message  # Ottieni l'oggetto Message dall'aggiornamento
    text = message.text  # Ottieni il testo del messaggio

    try:
        order_instance = Trade()

        # Estraggo la coppia di valute
        currency_pair = re.search(r"(\w+)/(\w+)", text)

        if currency_pair:
            # va bene anche solo currency_pair.group()
            order_instance.set_currency_pair = (
                f"{currency_pair.group(1)}{currency_pair.group(2)}"
            )

        # Estraggo il tipo di ordine (buy o sell)
        order_type = re.search(
            r"(buy|sell)( limit| stop| diretta a mercato)", text, re.IGNORECASE)
        if order_type:
            order_instance.set_order_type = order_type.group().lower()

        # Estraggo il prezzo di apertura
        opening_price = re.search(r"Prezzo\s+(\d+\.\d+)", text)
        if opening_price:
            order_instance.set_opening_price = float(opening_price.group(1))

        # Estraggo il prezzo di Stop Loss
        stop_loss = re.search(r"stop\s+loss.*?(\d+\.\d+)", text, re.IGNORECASE)
        if stop_loss:
            order_instance.set_stop_loss = float(stop_loss.group(1))

        # Estraggo il prezzo di Take Profit
        take_profit = re.search(
            r"take\s+profit.*?(\d+\.\d+)", text, re.IGNORECASE)
        if take_profit:
            order_instance.set_take_profit = float(take_profit.group(1))

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I wasn't able to extract useful informations from your message. 😕",
        )

    # For debugging
    extracted_order_info = {
        "Currency pair": order_instance.get_currency_pair,
        "Order type": order_instance.get_order_type,
        "Opening price": order_instance.get_opening_price,
        "Stop loss": order_instance.get_stop_loss,
        "Take profit": order_instance.get_take_profit,
    }
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=extracted_order_info,
    )
