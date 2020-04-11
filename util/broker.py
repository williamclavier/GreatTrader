from util.stock import Price
from util.logging import Log


class LiveBroker:
    def __init__(self, name, balance=1000, debug=False):
        self.balance = balance
        self.name = name
        self.debug = debug
        self.Log = Log(name)

    def Buy(self, symbol, amount=1):
        price = Price(symbol, amount)
        if self.haveEnoughMoney(price):
            self.Log.Buy(symbol, amount)
            # purchase stock
            self.decreaseBal(price)
            return True
        else:
            return False

    def Sell(self, symbol, amount=1):
        # Check if you have that many stocks available
        # Store data in file but store it in runtime once the program starts
        price = Price(symbol, amount)
        # Temp
        return price

    def Balance(self):
        return round(float(self.balance), 4)

    def Holdings(self):
        return None

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
