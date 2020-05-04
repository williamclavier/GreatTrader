import util.stock
from util.database import combine
from util.logging import Log
from pathlib import Path
import logging


class LiveBroker:
    def __init__(self, balance=100000, debug=False):
        self.start_bal = balance
        self.balance = balance
        self.debug = debug
        self.Log = Log()
        log_folder = Path("logs/")
        logging.basicConfig(
            filename=log_folder / "Transactions.log",
            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def buy(self, symbol, amount=1):
        price = util.stock.price(symbol, amount)
        if self.have_enough_money(price):
            # purchase stock
            self.decrease_bal(price)
            # Log it
            self.Log.buy(symbol, amount)
            self.logger.info("Buy: {} x{} @ ${} each. Balance: {} \
                    Holdings: {} Total: {}".format(
                        symbol, amount, price, self.balance, self.holdings(),
                        self.balance + self.holdings()))
            return True
        else:
            return False

    def sell(self, symbol, amount=1):
        # Check if you have that many stocks available
        price = util.stock.price(symbol, amount)
        trades = combine("amount")
        combined_list = {
            key: trades[0][key] - trades[1].get(key, 0)
            for key in trades[0].keys()
        }
        available = 0
        for ticker in combined_list:
            if ticker == symbol:
                available = combined_list[ticker]
        # used to be "if amount <= available:
        if amount <= available:
            self.Log.sell(symbol, amount)
            self.logger.info("Sell: {} x{} @ ${} each. Balance: {} \
                        Holdings: {} Total: {}".format(
                            symbol, amount, price, self.balance,
                            self.holdings(), self.balance + self.holdings()))
            return True
        else:
            return False

    def balance(self):
        return round(float(self.balance), 4)

    def holdings(self):
        # global Combined remove this later if no issues
        total = 0
        trades = combine('cost')
        # trades[0] = boughtList; trades[1] = soldList
        for stock in trades[0]:
            total -= trades[0][stock]
        for stock in trades[1]:
            total += trades[1][stock]
        # Now for unsold stock
        trades = combine('amount')
        # trades[0] = boughtList; trades[1] = soldList
        # combined_list is the difference in corresponding values
        combined_list = {
            key: trades[0][key] - trades[1].get(key, 0)
            for key in trades[0].keys()
        }
        subtotal = 0
        for stock in combined_list:
            subtotal += util.stock.price(stock, combined_list[stock])
        return round(subtotal + total, 4) + self.balance

    def have_enough_money(self, cost, amount=1):
        if self.balance >= round((cost * amount), 4):
            return True
        else:
            return False

    def decrease_bal(self, value):
        """
        Only enabled for debugging
        """
        self.balance = round(self.balance - value, 4)

    def increase_bal(self, value):
        """
        Only enabled for debugging
        """
        self.balance = round(self.balance + value, 4)
