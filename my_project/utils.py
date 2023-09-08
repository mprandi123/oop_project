from telegram import Update
from telegram.ext import ContextTypes
from my_project.TradeClass import Trade
import regex as re

# scrivere doc + controllare tipo dati


def extract_currency_pair(text: str) -> str:
    return re.search(r"(\w+)/(\w+)", text)


def extract_order_type(text: str) -> str:
    return re.search(r"(buy|sell)( limit| stop| diretta a mercato)", text, re.IGNORECASE)


def extract_opening_price(text: str) -> float:
    return re.search(r"Prezzo\s+(\d+\.\d+)", text)


def extract_stop_loss(text: str) -> float:
    return re.search(r"stop\s+loss.*?(\d+\.\d+)", text, re.IGNORECASE)


def extract_take_profit(text: str) -> float:
    return re.search(r"take\s+profit.*?(\d+\.\d+)", text, re.IGNORECASE)


async def message_parser(update: Update, context: ContextTypes.DEFAULT_TYPE, connection):
    """extract info from the message received on Telegram (update object)

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks

    """
    message = update.message  # Ottieni l'oggetto Message dall'aggiornamento
    text = message.text  # Ottieni il testo del messaggio

    # new order
    new_order = re.search(
        r"significa che bisogna piazzare un ordine pendente", text)
    # close open order
    close_open_order = re.search(r"CHIUDERE", text)
    # cancel order
    cancel_order = re.search(r"ANNULLARE", text)
    # modify opening price
    modify_op = re.search(r"MODIFICARE IL PREZZO DI INGRESSO", text)
    # modify stop loss
    modify_sl = re.search(r"MODIFICARE IL VALORE DI STOP LOSS", text)
    # modify take profit
    modify_tp = re.search(r"MODIFICARE IL VALORE DI TAKE PROFIT", text)
    # conferm opening
    conferm_opening_order = re.search(r"Aperto", text)

    if new_order:

        order_instance = Trade()

        currency_pair = extract_currency_pair(text=text)
        # va bene anche solo currency_pair.group()
        order_instance.set_currency_pair = (
            f"{currency_pair.group(1)}{currency_pair.group(2)}")

        order_type = extract_order_type(text=text)
        order_instance.set_order_type = order_type.group().lower()

        opening_price = extract_opening_price(text=text)
        order_instance.set_opening_price = float(opening_price.group(1))

        stop_loss = extract_stop_loss(text=text)
        order_instance.set_stop_loss = float(stop_loss.group(1))

        take_profit = extract_take_profit(text=text)
        order_instance.set_take_profit = float(take_profit.group(1))

        extracted_order_info = {
            "Currency pair": order_instance.get_currency_pair,
            "Order type": order_instance.get_order_type,
            "Opening price": order_instance.get_opening_price,
            "Stop loss": order_instance.get_stop_loss,
            "Take profit": order_instance.get_take_profit,
        }

        if extracted_order_info.values.all():
            order_instance.create_new_order(
                update=update, context=context, connection=connection)
        else:
            missing_info = [
                key for key in extracted_order_info.keys if extracted_order_info.values is None]
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"You didn't insert all information. {missing_info} missing"),
            )

        # for debug
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=extracted_order_info,
        )
"""
    elif close_open_order:
        
    elif cancel_order:
    elif modify_op:
    elif modify_sl:
    elif modify_tp:
    elif conferm_opening_order:
    

    
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I wasn't able to extract useful informations from your message. 😕",
        )
    """
