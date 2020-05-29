from typing import Dict

from src.logging import Log


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
        bought_list: Dict[str, int] = {}
        sold_list: Dict[str, int] = {}
    elif item.lower() == "cost":
        index = 4
        bought_list: Dict[str, float] = {}
        sold_list: Dict[str, float] = {}
    else:
        print("{} isn't a correct option. \
                (src.database.combine)".format(item))
        return None
    bought = Log().read("buy")
    sold = Log().read("sell")
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
