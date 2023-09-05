class Trade():
    # Costruttore -> definisco tutti gli attributi all'interno di __init__
    def __init__(self) -> None:
        # istanzio gli attributi
        self.currency_pair = "EUR/EUR"
        self.order_type = "BUY LIMIT"
        self.opening_price = 0
        self.stop_loss = 0
        self.take_profit = 0

    # Metodo per aprire un nuovo ordine a mercato o in pending 
    def create_new_order(self, currency_pair, order_type, opening_price, stop_loss, take_profit):
        pass
    
    # Metodo per modificare un ordine in pending
    def modify_order(self, currency_pair, order_type, opening_price):
        pass

    # Metodo per chiudere un ordine aperto
    def close_order(self, currency_pair, order_type, opening_price, stop_loss, take_profit):
        pass

    # Metodo per cancellare un ordine in pending
    def cancel_order(self, currency_pair, order_type, opening_price, stop_loss, take_profit):
        pass

    # Metodo per ignorare un ordine scritto male mandando avviso di errore
    def ignore_message(self, currency_pair, order_type, opening_price, stop_loss, take_profit):
        pass

    # (QUESTO PER TESTARE CHE FUNZIONI IL BOT) Metodo per confermare che un ordine in pending si è aperto con successo
    def confirm_open_order(self, currency_pair, order_type, opening_price, stop_loss, take_profit):
        pass