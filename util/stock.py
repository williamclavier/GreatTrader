import yfinance as yf
from datetime import datetime
import pandas as pd

# Add the ability to get price from a certain date
def price(symbol, amount):
    """Gives the current stock price.

    Arguments:
    ticker -- the stock ticker
    amount -- the quantity of stocks
    """
    symbol = yf.Ticker(symbol)
    current_time = datetime.now().strftime("%H:%M:%S").split(":")
    cost = 0
    if int(current_time[0]) >= 9 & int(current_time[1]) >= 30:
        if int(current_time[0]) < 16:
            data = symbol.history(period="intraday", interval='1m')
            cost = data['Close'][(len(data['Close']) - 1)]
    else:
        data = symbol.history(period="1mo", interval="1d")
        cost = data['Close'][(len(data['Close']) - 1)]
    return round(float(cost) * amount, 4)


def top_gainers(amount=10):
    """Gathers the top earners from yahoo finance.

    Keyword Arguments:
    amount -- the amount of stocks to return (default 10)

    Returns:
    tickers -- the top tickers on the list as a list
    """
    data = pd.read_html('https://finance.yahoo.com/gainers')[0]['Symbol']
    return data.head(amount)
