from util.stock import Price
from util.logging import Log


class LiveBroker:
    def __init__(self, balance=100000, debug=False):
        self.balance = balance
        self.debug = debug
        self.Log = Log()

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
        self.Log.Sell(symbol, amount)
        # Check if you have that many stocks available
        # Store data in file but store it in runtime once the program starts
        price = Price(symbol, amount)
        # Temp
        return price

    def Balance(self):
        return round(float(self.balance), 4)

    def Holdings(self):
        Bought = self.Log.Read("buy")
        BoughtList = {}
        Total = 0
        for trade in Bought:
            if trade[2] in BoughtList:
                val = BoughtList[trade[2]]
                BoughtList[trade[2]] = val + trade[4]
            else:
                BoughtList[trade[2]] = trade[4]
        Sold = self.Log.Read("sell")
        SoldList = {}
        for trade in Sold:
            if trade[2] in SoldList:
                val = SoldList[trade[2]]
                SoldList[trade[2]] = val + trade[4]
            else:
                SoldList[trade[2]] = trade[4]
        for stock in BoughtList:
            Total -= BoughtList[stock]
        for stock in SoldList:
            Total += SoldList[stock]
        # Now for unsold stock
        SoldList = {}
        BoughtList = {}
        BoughtList = {}
        for trade in Bought:
            if trade[2] in BoughtList:
                val = BoughtList[trade[2]]
                BoughtList[trade[2]] = val + trade[3]
            else:
                BoughtList[trade[2]] = trade[3]
        Sold = self.Log.Read("sell")
        SoldList = {}
        for trade in Sold:
            if trade[2] in SoldList:
                val = SoldList[trade[2]]
                SoldList[trade[2]] = val + trade[3]
            else:
                SoldList[trade[2]] = trade[3]
        Combined = {
            key: BoughtList[key] - SoldList.get(key, 0)
            for key in BoughtList.keys()
        }
        Subtotal = 0
        for stock in Combined:
            Subtotal += Price(stock, Combined[stock])
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
