
class LiveBroker:
    def __init__(self, API, balance=1000):
        self.balance = balance
        self.api = API
        self.filename = "virtual-{}.json"

    def Price(self, symbol, amount=1):
        data, meta_data = self.api.get_intraday(symbol=symbol, interval="1min")
        cost = data['4. close'][0]
        return (float(cost) * amount)

    def Buy(self, symbol, amount=1):
        price = self.Price(symbol, amount)
        if self.haveEnoughMoney(price):
            # includes logging to json
            # purchase stock
            self.deductBalance(price)
            return True
        else:
            return False

    def Sell(self, symbol, amount=1):
        # Check if you have that many stocks available
        # Store data in file but store it in runtime once the program starts
        price = self.Price(symbol, amount)
        

    def Balance(self):
        return self.balance

    def haveEnoughMoney(self, cost, amount=1):
        if self.balance >= (cost * amount):
            return True
        else:
            return False

    def decreaseBal(self, value):
        self.balance -= value

    def increaseBal(self, value):
        self.balance += value
