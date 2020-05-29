# Example Trading Strategy Code
# Use this to make more!
from src.strategy_parent_class import *
import pandas as pd
# Inspired by https://youtu.be/SEQbb8w7VTw
# This shows how you can find any strategy online and replicate it easily


class Strategy(ParentStrategy):
    """Uses dual simple moving average crossover.

    Arguments:
    ticker -- the stock's ticker
    """
    def __init__(self, ticker):
        super().__init__(ticker)
        self.incremental = True
        self.name = "DualMovingAverage"
        self.ticker = ticker
        self.limited_data = []
        # limit it to the last 200 days of data for efficiency because this doesn't need much past data
        # self.limited_data["Close"] = data[len(self.limited_data) - 200:]
        """
        self.all_time = super().stock_data()
        self.data_30day = pd.DataFrame()
        self.data_100day = pd.DataFrame()
        self.data_30day["Close"] = super().stock_data()["Close"].rolling(window=30).mean()
        self.data_100day["Close"] = super().stock_data()["Close"].rolling(window=100).mean()
        self.data = pd.DataFrame()
        self.data[ticker] = self.all_time['Close']
        self.data["SMA30"] = self.data_30day['Close']
        self.data["SMA100"] = self.data_100day['Close']
        buy_indicators, sell_indicators = self.buy_sell()
        self.data["Buy Indicators"] = buy_indicators
        self.data["Sell Indicators"] = sell_indicators
        super().plot_data(self.data)
        """

    def main(self, data):
        self.limited_data = pd.DataFrame()
        self.limited_data["Close"] = data
        sma30 = pd.DataFrame()
        sma100 = pd.DataFrame()
        sma30["Close"] = self.limited_data["Close"].rolling(window=30).mean()
        sma100["Close"] = self.limited_data["Close"].rolling(window=100).mean()
        flag = 0.0
        for i in range(len(self.limited_data)):
            if sma30["Close"][i] > sma100["Close"][i]:
                if flag != 1.0:
                    # Buy
                    flag = 1.0
                else:
                    # Hold
                    flag = 0.0
            elif sma30["Close"][i] < sma100["Close"][i]:
                if flag != -1.0:
                    # Sell
                    flag = -1.0
                else:
                    # Hold
                    flag = 0.0

        return flag
