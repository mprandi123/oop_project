from telegram import Update
from telegram.ext import ContextTypes
import logging


class Trade:

    # Costruttore -> definisco tutti gli attributi all'interno di __init__
    def __init__(self) -> None:
        # istanzio gli attributi
        self.currency_pair = "EUR/EUR"
        self.order_type = "BUY DIRETTA A MERCATO"
        self.opening_price = 0.0
        self.stop_loss = 0.0
        self.take_profit = 0.0
        self.lots = 0.05

    def set_currency_pair(self, currency_pair):
        self.currency_pair = currency_pair

    def get_currency_pair(self):
        return self.currency_pair

    def set_order_type(self, order_type):
        self.order_type = order_type

    def get_order_type(self):
        return self.order_type

    def set_opening_price(self, opening_price):
        self.opening_price = opening_price

    def get_opening_price(self):
        return self.opening_price

    def set_stop_loss(self, stop_loss):
        self.stop_loss = stop_loss

    def get_stop_loss(self):
        return self.stop_loss

    def set_take_profit(self, take_profit):
        self.take_profit = take_profit

    def get_take_profit(self):
        return self.take_profit

    def set_lots(self, lots=0.05):
        self.lots = lots

    def get_lots(self):
        return self.lots

    async def create_new_order(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        connection,
    ):
        """_summary_

        Args:
            update (Update): _description_
            context (ContextTypes.DEFAULT_TYPE): _description_
            connection: _description_
        """
        # enters trade on to MetaTrader account
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Entering trade on MetaTrader Account ...",
        )

        try:
            # executes buy market execution order
            if self.order_type == "buy diretta a mercato":
                result = await connection.create_market_buy_order(
                    self.currency_pair,
                    self.lots,
                    self.stop_loss,
                    self.take_profit,
                )
            # executes buy limit order
            elif self.order_type == "buy limit":
                result = await connection.create_limit_buy_order(
                    self.currency_pair,
                    self.lots,
                    self.opening_price,
                    self.stop_loss,
                    self.take_profit,
                )

            # executes buy stop order
            elif self.order_type == "buy stop":
                result = await connection.create_stop_buy_order(
                    self.currency_pair,
                    self.lots,
                    self.opening_price,
                    self.stop_loss,
                    self.take_profit,
                )
                result["orderId"]
            # executes sell market execution order
            elif self.order_type == "sell diretta a mercato":
                result = await connection.create_market_sell_order(
                    self.currency_pair,
                    self.lots,
                    self.stop_loss,
                    self.take_profit,
                )
            # executes sell limit order
            elif self.order_type == "sell limit":
                result = await connection.create_limit_sell_order(
                    self.currency_pair,
                    self.lots,
                    self.opening_price,
                    self.stop_loss,
                    self.take_profit,
                )
            # executes sell stop order
            elif self.order_type == "sell stop":
                result = await connection.create_stop_sell_order(
                    self.currency_pair,
                    self.lots,
                    self.opening_price,
                    self.stop_loss,
                    self.take_profit,
                )

            # sends success message to user
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Trade entered successfully! 💰",
            )

            # prints success message to console
            logging.info("\nTrade entered successfully!")
            logging.info("Result Code: {}\n".format(result["stringCode"]))

        except Exception as error:
            logging.error(f"\nTrade failed with error: {error}\n")

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"There was an issue 😕\n\nError Message:\n{error}",
            )



# Note: Qua ho scelto di spostare queste funzioni fuori dalla classe perchè se no avrei dovuto creare una istanza di Trade (per poter chiamare questa funzione da Utils.py) senza usarla e mi sembrava poco elegante.


async def close_order(update: Update, context: ContextTypes.DEFAULT_TYPE, connection, position_id):
    """Close order with its id. 

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks;
        connection: istance from account.get_rpc_connection() to connect with MetaApi;
        open_positions (list of dicts): open positions in my MT4 account;
        position_to_close (list of tuples): position (currency pair and price) to close
    """
    try:
        result = await connection.close_position(position_id=position_id)

        # sends success message to user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Trade closed successfully!",
        )

        logging.info("\nTrade entered successfully!")
        logging.info(f"Result Code: {result['stringCode']}\n")

    except Exception as error:
        logging.error(f"\nClosed trade failed with error: {error}\n")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There was an issue 😕\n\nError Message:\n{error}",
        )


async def annul_order(update: Update, context: ContextTypes.DEFAULT_TYPE, connection, position_id):
    """Annul pending order with its id

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks;
        connection (_type_): istance from account.get_rpc_connection() to connect with MetaApi;
        position_id (_type_): position to cancel
    """
    try:
        result = await connection.cancel_order(position_id)

        # sends success message to user
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Order closed successfully!",
        )

        logging.info("\nTrade entered successfully!")
        logging.info(f"Result Code: {result['stringCode']}\n")

    except Exception as error:
        logging.error(f"\nClosed trade failed with error: {error}\n")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There was an issue 😕\n\nError Message:\n{error}",
        )


async def modify_opening_price(update: Update, context: ContextTypes.DEFAULT_TYPE, connection, position_id, opening_price):
    """modify the opening price of an order still not open

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks;
        connection: istance from account.get_rpc_connection() to connect with MetaApi;
        position_id (int): position id to modify
    """
    try:
        result = await connection.modify_order(order_id=position_id, open_price=opening_price)

        # sends success message to user
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Order modified successfully!")

        logging.info("\nOrder modified successfully!")
        logging.info(f"Result Code: {result['stringCode']}\n")

    except Exception as error:
        logging.error(f"\nModified trade failed with error: {error}\n")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There was an issue 😕\n\nError Message:\n{error}",
        )


async def modify_stop_loss(update: Update, context: ContextTypes.DEFAULT_TYPE, connection, position_id, opening_price, stop_loss):
    """modify the stop loss of orders with a specific currency pair

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks;
        connection: istance from account.get_rpc_connection() to connect with MetaApi;
        position_id (int): position id to modify
    """
    try:
        result = await connection.modify_order(position_id, open_price=opening_price, stop_loss=stop_loss)

        # sends success message to user
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Order modified successfully!")

        logging.info("\nOrder modified successfully!")
        logging.info(f"Result Code: {result['stringCode']}\n")

    except Exception as error:
        logging.error(f"\nModified trade failed with error: {error}\n")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There was an issue 😕\n\nError Message:\n{error}",
        )


async def modify_take_profit(update: Update, context: ContextTypes.DEFAULT_TYPE, connection, position_id, opening_price, take_profit):
    """modify the take profit of orders with a specific currency pair

    Args:
        update: update from Telegram
        context: CallbackContext object that stores commonly used objects in handler callbacks;
        connection: istance from account.get_rpc_connection() to connect with MetaApi;
        position_id (int): position id to modify
    """
    try:
        result = await connection.modify_order(position_id, open_price=opening_price, take_profit=take_profit)

        # sends success message to user
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Order modified successfully!")

        logging.info("\nOrder modified successfully!")
        logging.info(f"Result Code: {result['stringCode']}\n")

    except Exception as error:
        logging.error(f"\nModified trade failed with error: {error}\n")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There was an issue 😕\n\nError Message:\n{error}",
        )