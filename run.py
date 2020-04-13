# this is currently for testing but will be where the main app is soon!!!
from util.broker import LiveBroker
from datetime import datetime as dt
from time import sleep

Broker = LiveBroker()
# Broker.Buy("GOOG", 6)
# Broker.Sell("GOOG", 5)
try:
    Start = Broker.startBalance
    while True:
        Holdings = Broker.Holdings()
        Percent = round(((Holdings - Start) / Start) * 100, 4)
        if Percent > 0:
            percentString = "+{}%".format(Percent)
        else:
            percentString = "{}%".format(Percent)
        print("{} --> $ {}    ({})".format(
            dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            Holdings, percentString))
        sleep(1)
except KeyboardInterrupt:
    pass
