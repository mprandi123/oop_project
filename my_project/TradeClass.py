from telegram import Update
from telegram.ext import ContextTypes


class Trade:
    LOTS = 0.07

    # Costruttore -> definisco tutti gli attributi all'interno di __init__
    def __init__(self) -> None:
        # istanzio gli attributi
        self.currency_pair = "EUR/EUR"
        self.order_type = "BUY DIRETTA A MERCATO"
        self.opening_price = 0.0
        self.stop_loss = 0.0
        self.take_profit = 0.0

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

    # Metodo per aprire un nuovo ordine a mercato o in pending
    async def create_new_order(
        self,
        LOTS,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        connection,
        logger,
    ):
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
                    LOTS,
                    self.stop_loss,
                    self.take_profit,
                )
            # executes buy limit order
            elif self.order_type == "buy limit":
                result = await connection.create_limit_buy_order(
                    self.currency_pair,
                    LOTS,
                    self.opening_price,
                    self.stop_loss,
                    self.take_profit,
                )
            # executes buy stop order
            elif self.order_type == "buy stop":
                result = await connection.create_stop_buy_order(
                    self.currency_pair,
                    LOTS,
                    self.opening_price,
                    self.stop_loss,
                    self.take_profit,
                )
            # executes sell market execution order
            elif self.order_type == "sell diretta a mercato":
                result = await connection.create_market_sell_order(
                    self.currency_pair,
                    LOTS,
                    self.stop_loss,
                    self.take_profit,
                )
            # executes sell limit order
            elif self.order_type == "sell limit":
                result = await connection.create_limit_sell_order(
                    self.currency_pair,
                    LOTS,
                    self.opening_price,
                    self.stop_loss,
                    self.take_profit,
                )
            # executes sell stop order
            elif self.order_type == "sell stop":
                result = await connection.create_stop_sell_order(
                    self.currency_pair,
                    LOTS,
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
            logger.info("\nTrade entered successfully!")
            logger.info("Result Code: {}\n".format(result["stringCode"]))

        except Exception as error:
            logger.error(f"\nTrade failed with error: {error}\n")

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"There was an issue 😕\n\nError Message:\n{error}",
            )

    def close_order(
        self, currency_pair, order_type, opening_price, stop_loss, take_profit,
    ):
        pass

    def cancel_order(
        self, currency_pair, order_type, opening_price, stop_loss, take_profit,
    ):
        pass

    def modify_opening_price(
        self, currency_pair, order_type, opening_price,
    ):
        pass

    def modify_stop_loss(
        self, currency_pair, order_type, opening_price,
    ):
        pass

    def modify_take_profit(
        self, currency_pair, order_type, opening_price,
    ):
        pass

    def confirm_open_order(
        self, currency_pair, order_type, opening_price, stop_loss, take_profit,
    ):
        pass
