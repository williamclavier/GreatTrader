import util.stock
from util.database import combine
from util.logging import Log
from pathlib import Path
import logging


class LiveBroker:
    """Virtual broker to trade with.

    Keyword Arguments:
    balance -- the broker account start balance (default 100000)
    debug -- enables debug logging (default False)
    """
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

    def buy(self, ticker, amount):
        """Purchases stocks.

        Arguments:
        ticker -- the ticker to be purchased
        amount -- the quantity of stocks to be purchased
        """
        price = util.stock.price(ticker, amount)
        if self.have_enough_money(price):
            # purchase stock
            self.decrease_bal(price)
            # Log it
            self.Log.buy(symbol, amount)
            self.logger.info("Buy: {} x{} @ ${} each. Balance: {} \
                    Holdings: {} Total: {}".format(
                        symbol, amount, price, self.balance, self.holdings(),
                        self.valuation()))
            return True
        else:
            return False

    def sell(self, ticker, amount):
        """Sells stocks.

        Arguments:
        ticker -- the ticker to be sold
        amount -- the quantity of stocks to be sold
        """
        # Check if you have that many stocks available
        price = util.stock.price(ticker, amount)
        trades = combine("amount")
        combined_list = {
            key: trades[0][key] - trades[1].get(key, 0)
            for key in trades[0].keys()
        }
        available = 0
        for owned_ticker in combined_list:
            if owned_ticker == ticker:
                available = combined_list[owned_ticker]
        # used to be "if amount <= available:
        if amount <= available:
            self.Log.sell(symbol, amount)
            self.logger.info("Sell: {} x{} @ ${} each. Balance: {} \
                        Holdings: {} Total: {}".format(
                            ticker, amount, price, self.balance,
                            self.holdings(), self.balance + self.holdings()))
            return True
        else:
            return False

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
        if amount == "total":
            return round(subtotal + total, 4) + self.balance
        elif amount == "temp" or amount == "current":
            return round(subtotal, 4)
        else:
            return round(subtotal + total, 4) + self.balance

    @staticmethod
    def possessions():
        trades = combine("amount")
        combined_list = {
            key: trades[0][key] - trades[1].get(key, 0)
            for key in trades[0].keys()
        }
        return combined_list

    def have_enough_money(self, cost, amount):
        """Performs simple math to verify you can afford the stocks.

        Arguments:
        cost -- the cost of one singular stock
        amount -- the amount of stocks to be purchased

        Returns:
        Bool -- if it is affordable, will return True
        """
        if self.balance >= round((cost * amount), 4):
            return True
        else:
            return False
