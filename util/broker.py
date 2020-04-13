from util.stock import Price
from util.database import Combine
from util.logging import Log
from pathlib import Path
import logging


class LiveBroker:
    def __init__(self, balance=100000, debug=False):
        self.startBalance = balance
        self.balance = balance
        self.debug = debug
        self.Log = Log()
        logfolder = Path("log/")
        logging.basicConfig(
            filename=logfolder / "Transactions.log",
            format='%(asctime)s %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def Buy(self, symbol, amount=1):
        price = Price(symbol, amount)
        if self.haveEnoughMoney(price):
            self.Log.Buy(symbol, amount)
            self.logger.info("Buy: {} x{} @ ${} each. Balance: {} \
                    Holdings: {} Total: {}".format(
                        symbol, amount, price, self.balance, self.Holdings(),
                        self.balance + self.Holdings()))
            # purchase stock
            self.decreaseBal(price)
            return True
        else:
            return False

    def Sell(self, symbol, amount=1):
        # Check if you have that many stocks available
        price = Price(symbol, amount)
        Trades = Combine("amount")
        CombinedList = {
            key: Trades[0][key] - Trades[1].get(key, 0)
            for key in Trades[0].keys()
        }
        for ticker in CombinedList:
            if ticker == symbol:
                available = CombinedList[ticker]
        if amount <= available:
            self.Log.Sell(symbol, amount)
            self.logger.info("Sell: {} x{} @ ${} each. Balance: {} \
                        Holdings: {} Total: {}".format(
                            symbol, amount, price, self.balance,
                            self.Holdings(), self.balance + self.Holdings()))
            return True
        else:
            return False

    def Balance(self):
        return round(float(self.balance), 4)

    def Holdings(self):
        global Combined
        Total = 0
        Trades = Combine('cost')
        # Trades[0] = boughtList; Trades[1] = soldList
        for stock in Trades[0]:
            Total -= Trades[0][stock]
        for stock in Trades[1]:
            Total += Trades[1][stock]
        # Now for unsold stock
        Trades = Combine('amount')
        # Trades[0] = boughtList; Trades[1] = soldList
        # CombinedList is the difference in corresponding values
        CombinedList = {
            key: Trades[0][key] - Trades[1].get(key, 0)
            for key in Trades[0].keys()
        }
        Subtotal = 0
        for stock in CombinedList:
            Subtotal += Price(stock, CombinedList[stock])
        return round(Subtotal + Total, 4) + self.balance

    def haveEnoughMoney(self, cost, amount=1):
        if self.balance >= round((cost * amount), 4):
            return True
        else:
            return False

    def decreaseBal(self, value):
        """
        Only enabled for debugging
        """
        self.balance = round(self.balance - value, 4)

    def increaseBal(self, value):
        """
        Only enabled for debugging
        """
        self.balance = round(self.balance + value, 4)
