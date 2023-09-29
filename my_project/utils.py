from telegram import Update
from telegram.ext import ContextTypes
from my_project.trade import Trade, close_order, annul_order, modify_opening_price, modify_stop_loss, modify_take_profit
import regex as re
import logging

# scrivere doc + controllare tipo dati


def extract_id(open_orders, position_target) -> int:
    """ extract id from matching between open_orders in MT4 and infos in position_target

    Args:
        open_orders (list of dicts): list of all open position in my MT4 account
        position_target (list): list of currency_pair and opening_price to define for which position extrtact id. position_target[t][0] = currency_pair (without / between currency), position_target[t][1] = price, 

    Returns:
        int: position target's id
    """
    try:
        # This block is necessary for modify sl or tp to extract more order_id
        if isinstance(position_target, str):
            same_currency = []
            for i in range(len(open_orders)):
                if (position_target == open_orders[i]["symbol"]):
                    same_currency.append(
                        [open_orders[i]["id"], open_orders[i]["openPrice"]])
            return same_currency

        # WARNING: take a look to the spread and the difference from signal to open_position[]["openPrice"]
        for i in range(len(open_orders)):
            for t in range(len(position_target)):
                # if position_target's currency_pair is equal to symbol in the i-th dict & position_target's opening price is equal to openPrice in the i-th dict, save the index i
                if (position_target[t][0] == open_orders[i]["symbol"]) & (round(float(position_target[t][1]), 4) == round(float(open_orders[i]["openPrice"]), 4)):
                    return open_orders[i]["id"]

    except Exception as error:
        logging.error(f"{error}. {position_target} not found!")


def extract_currency_pair(text: str) -> str:
    currency_pair = re.search(r"(\w+)/(\w+)", text)
    return f"{currency_pair.group(1)}{currency_pair.group(2)}"


def extract_order_type(text: str) -> str:
    return re.search(r"(buy|sell)( limit| stop| diretta a mercato)", text, re.IGNORECASE)


def extract_opening_price(text: str) -> float:
    return re.search(r"Prezzo\s+(\d+\.\d+)", text)


def extract_stop_loss(text: str) -> float:
    return re.search(r"stop\s+loss.*?(\d+\.\d+)", text, re.IGNORECASE)


def extract_take_profit(text: str) -> float:
    return re.search(r"take\s+profit.*?(\d+\.\d+)", text, re.IGNORECASE)


def extract_pairs_currency_price(text: str) -> list:
    """It's used for closing multiple open positions. Extract_opening_price() is specialised for create_new_order.

    Args:
        text (str): Riceved message with orders to close. 

    Returns:
        list: list of (currency_pair, opening_price)
    """
    # regex model for pairs: curreny_pair & opening_price
    # Guarda appunti Info -> Regex
    pattern = r"(\w+)/(\w+)\s+\(([\d.]+)\)"

    matches = re.findall(pattern, text)

    pairs_currencies_prices = [
        (str(match[0]+match[1]), float(match[2])) for match in matches]

    return pairs_currencies_prices


def extract_op_to_modify(text: str) -> float:
    op_final = re.search(r"\sA\s+(\d+\.\d+)", text)
    op_to_modify = re.search(r"DA\s+(\d+\.\d+)", text)

    return op_to_modify.group(), op_final.group()


async def message_parser(update: Update, context: ContextTypes.DEFAULT_TYPE, connection):
    """extract info from the message received on Telegram (update object)

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks

    """
    message = update.message  # Ottieni l'oggetto Message dall'aggiornamento
    text = message.text  # Ottieni il testo del messaggio

    # create new order
    if re.search(r"significa che bisogna piazzare un ordine pendente", text):

        order_instance = Trade()

        currency_pair = extract_currency_pair(text=text)
        # va bene anche solo currency_pair.group()
        order_instance.set_currency_pair(currency_pair=currency_pair)

        order_type = extract_order_type(text=text)
        order_instance.set_order_type(order_type.group().lower())

        opening_price = extract_opening_price(text=text)
        order_instance.set_opening_price(float(opening_price.group(1)))

        stop_loss = extract_stop_loss(text=text)
        order_instance.set_stop_loss(float(stop_loss.group(1)))

        take_profit = extract_take_profit(text=text)
        order_instance.set_take_profit(float(take_profit.group(1)))

        extracted_order_info = {
            "Currency pair": order_instance.get_currency_pair(),
            "Order type": order_instance.get_order_type(),
            "Opening price": order_instance.get_opening_price(),
            "Stop loss": order_instance.get_stop_loss(),
            "Take profit": order_instance.get_take_profit(),
        }

        # for debug
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Extracted infos: {extracted_order_info}"
        )

        await order_instance.create_new_order(update=update, context=context, connection=connection)

    # close open order
    elif re.search(r"CHIUDERE\s+MANUALMENTE", text):
        position_to_close = extract_pairs_currency_price(text=text)
        open_positions = await connection.get_positions()
        position_id = extract_id(
            open_orders=open_positions, position_target=position_to_close)

        await close_order(update=update, context=context, connection=connection, position_id=position_id)

    # annull order
    elif re.search(r"ANNULLARE", text):
        position_to_annul = extract_pairs_currency_price(text=text)
        open_orders = await connection.get_orders()
        position_id = extract_id(
            open_orders=open_orders, position_target=position_to_annul)

        await annul_order(update=update, context=context, connection=connection, position_id=position_id)

    # modify opening price
    elif re.search(r"MODIFICARE IL PREZZO DI INGRESSO", text):
        order_type = extract_order_type(text=text)
        currrency_to_modify_op = extract_currency_pair(text=text)
        price_to_modify = extract_op_to_modify(text=text)
        open_orders = await connection.get_orders()
        position_to_modify = [
            [str(currrency_to_modify_op), float(price_to_modify[0].split()[1])]]
        position_id = extract_id(
            open_orders=open_orders, position_target=position_to_modify)

        if position_id:
            await modify_opening_price(update=update, context=context, connection=connection, position_id=position_id, opening_price=float(price_to_modify[1].split()[1]))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"I can't find this position {position_to_modify} on your MT4 account")

    # modify stop loss e take profit
    elif re.search(r"MODIFICARE IL VALORE DI", text):
        position_to_modify = extract_currency_pair(text=text)
        open_orders = await connection.get_orders()
        position_id = extract_id(
            open_orders=open_orders, position_target=position_to_modify)
        price = re.search(r"a\s+([\d.]+)", text).group(1)

        for i in range(len(position_id)):
            if re.search(r"STOP LOSS", text):
                await modify_stop_loss(update=update, context=context, connection=connection, position_id=position_id[i][0], opening_price=position_id[i][1], stop_loss=float(price))
            else:
                await modify_take_profit(update=update, context=context, connection=connection, position_id=position_id[i][0], opening_price=position_id[i][1], take_profit=float(price))

    # conferm opening
    elif re.search(r"Livello di ingresso", text):
        position_to_conferm = extract_currency_pair(text=text)
        open_positions = await connection.get_positions()
        price = float(
            re.search(r"Livello di ingresso\s+([\d.]+)", text).group(1))

        for i in range(len(open_positions)):
            if ((position_to_conferm == open_positions[i]["symbol"]) & (price == round(open_positions[i]["openPrice"], 4))):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Your order {position_to_conferm} {price} has been opened. 💰")
                return

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your order {position_to_conferm} {price} hasn't been opened. 😕")

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I wasn't able to extract useful informations from your message. 😕",
        )
