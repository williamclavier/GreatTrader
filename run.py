# this is currently for testing but will be where the main app is soon!!!
from util.broker import LiveBroker

Broker = LiveBroker()
# Broker.Buy("GOOG", 6)
# Broker.Sell("GOOG", 5)
print(Broker.Holdings())
