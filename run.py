# this is currently for testing but will be where the main app is soon!!!
from src.broker import LiveBroker
from src.stock import top_gainers
from datetime import datetime as dt
from time import sleep

Broker = LiveBroker()
Broker.buy("GOOG", 6)
Broker.sell("GOOG", 4)
# this is so we don't get too many different stocks at one period of time
print(Broker.holdings(amount="total"))
print(Broker.holdings(amount="temp"))
"""
amountNeeded = 5 - len(Broker.possessions())
print(top_gainers(amountNeeded))

try:
    Start = Broker.start_bal
    while True:
        holdings = Broker.holdings()
        Percent = round(((holdings - Start) / Start) * 100, 4)
        if Percent > 0:
            percentString = "+{}%".format(Percent)
        else:
            percentString = "{}%".format(Percent)
        print("{} --> $ {}    ({})".format(
            dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            holdings, percentString))
        sleep(1)
except KeyboardInterrupt:
    pass"""
