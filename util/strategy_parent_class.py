import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")


class Parent_Strategy:
    """Base parent class for all strategies.

    Arguments:
    ticker -- the stock's ticker
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock_object = yf.Ticker(self.ticker)
        self.historical_data = self.stock_object.history(period="max")

    def stock_data(self, period="max"):
        """Gathers past data on the stock.

        Keyword Arguments:
        period -- the period of time (default "max")
        """
        stock_data = self.stock_object.history(period=period)
        return stock_data

    def plot_data(self, data):
        """Plots stock history using matplotlib.

        Arguments:
        data -- the data sets you would like to plot. Ex: ["GOOG", data]
        """
        plt.figure(figsize=(12.5, 5.5))
        # Finds the start date to label the x-axis with from supplied data_sets
        """
        longest_data_set = ""
        max_length = 0
        data_set_index = 0
        for data_set in data:
            plt.plot(data_set[1], label=data_set[0])
            if len(data_set[1]) > longest_data_set:
                longest_data_set = data_set_index
                max_length = len(data_set[1])
            data_set_index += 1
        """
        for col in data.columns:
            # potentially should change this to .startswith()
            if "Buy" in col:
                plt.scatter(data.index, data[col], label="Buy", marker="^",
                            color="green")
            elif "Sell" in col:
                plt.scatter(data.index, data[col], label="Sell", marker="v",
                            color="red")
            else:
                plt.plot(data[col], label=col, alpha=0.35)
        start_date = str(data.index[0]).split('-')
        plt.subplots_adjust(bottom=0.1)
        plt.title("{} Close Price History".format(self.ticker))
        plt.xlabel("{}/{}/{} to {}/{}/{}".format(start_date[1], start_date[2].split(" ")[0],
                                                    start_date[0],
                                                    dt.now().month,
                                                    dt.now().day,
                                                    dt.now().year))
        plt.ylabel("Close Price USD ($)")
        plt.legend(loc='upper left')
        plt.show()
