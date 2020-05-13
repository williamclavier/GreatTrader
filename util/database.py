from util.logging import Log


def combine(item):
    """Combines the bought and sold database data.

    Arguments:
    column -- the column to gather data from in the bought and sold tables

    Returns:
    trades -- [bought_list, sold_list]
    """
    # the second index is the ticker
    if item.lower() == "amount":
        index = 3
    elif item.lower() == "cost":
        index = 4
    else:
        print("{} isn't a correct option. \
                (util.database.combine)".format(item))
        return None
    bought = Log().read("buy")
    sold = Log().read("sell")
    sold_list = {}
    bought_list = {}
    for trade in bought:
        # trade: ('2020-04-11', '19:01:34', 'SPY', 3, 834.6)
        if trade[2] in bought_list:
            val = bought_list[trade[2]]
            bought_list[trade[2]] = val + trade[index]
        else:
            bought_list[trade[2]] = trade[index]
    for trade in sold:
        # trade: ('2020-04-11', '19:01:34', 'SPY', 3, 834.6)
        if trade[2] in sold_list:
            val = sold_list[trade[2]]
            sold_list[trade[2]] = val + trade[index]
        else:
            sold_list[trade[2]] = trade[index]
    trades = [bought_list, sold_list]
    return trades
