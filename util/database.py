from util.logging import Log

Log = Log()


def Combine(item):
    if item.lower() == "date":
        index = 0
    elif item.lower() == "time":
        index = 1
    # 2 is the Ticker
    elif item.lower() == "amount":
        index = 3
    elif item.lower() == "cost":
        index = 4
    else:
        print("{} isn't a correct option. \
                (util.database.findDifference".format(item))
        return None
    Bought = Log.Read("buy")
    Sold = Log.Read("sell")
    soldList = {}
    boughtList = {}
    for trade in Bought:
        # trade: ('2020-04-11', '19:01:34', 'SPY', 3, 834.6)
        if trade[2] in boughtList:
            val = boughtList[trade[2]]
            boughtList[trade[2]] = val + trade[index]
        else:
            boughtList[trade[2]] = trade[index]
    for trade in Sold:
        # trade: ('2020-04-11', '19:01:34', 'SPY', 3, 834.6)
        if trade[2] in soldList:
            val = soldList[trade[2]]
            soldList[trade[2]] = val + trade[index]
        else:
            soldList[trade[2]] = trade[index]
    Trades = [boughtList, soldList]
    return Trades
