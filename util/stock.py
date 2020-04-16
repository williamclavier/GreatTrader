import yfinance as yf
from datetime import datetime
import pandas as pd


def Price(symbol, amount=1):
    symbol = yf.Ticker(symbol)
    currentTime = datetime.now().strftime("%H:%M:%S").split(":")
    if (int(currentTime[0]) >= 9 & int(currentTime[1]) >= 30):
        if (int(currentTime[0]) < 16):
            data = symbol.history(period="intraday", interval='1m')
            cost = data['Close'][(len(data['Close']) - 1)]
    else:
        data = symbol.history(period="1mo", interval="1d")
        cost = data['Close'][(len(data['Close']) - 1)]
    return round(float(cost) * amount, 4)


def TopGainers(amount=10):
    data = pd.read_html('https://finance.yahoo.com/gainers')[0]['Symbol']
    return data.head(amount)
