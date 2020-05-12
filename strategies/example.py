# Example Trading Strategy Code
# Use this to make more!
from util.strategy_parent_class import *
# Inspired by https://youtu.be/SEQbb8w7VTw
# This shows how you can find any strategy online and replicate it easily
class Strategy(Parent_Strategy):
    """Uses dual simple moving average crossover.

    Arguments:
    ticker -- the stock's ticker
    """
    def __init__(self, ticker, data):
        super().__init__(ticker)
        self.ticker = ticker
        self.limited_data = pd.DataFrame()
        self.limited_data["Close"] = data
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

    def main(self):
        SMA30 = pd.DataFrame()
        SMA100 = pd.DataFrame()
        #all_data = pd.DataFrame()
        SMA30["Close"] = self.limited_data["Close"].rolling(window=30).mean()
        SMA100["Close"] = self.limited_data["Close"].rolling(window=100).mean()
        #all_data[self.ticker] = self.limited_data
        #all_data["SMA30"] = SMA30["Close"]
        #all_data["SMA100"] = SMA100["Close"]
        flag = 0
        for i in range(len(self.limited_data)):
            if SMA30["Close"][i] > SMA100["Close"][i]:
                if flag != 1:
                    flag = 1
            elif SMA30["Close"][i] < SMA100["Close"][i]:
                if flag != -1:
                    flag = -1
        """
        if flag == 1:
            #print("Buy")
            return 1.0
        elif flag == -1:
            #print("Sell")
            return -1.0
        """

    def buy_sell(self):
        sig_price_buy = []
        sig_price_sell = []
        flag = 0

        for i in range(len(self.data)):
            if self.data_30day['Close'][i] > self.data_100day['Close'][i]:
                if flag != 1:
                    sig_price_buy.append(self.data[self.ticker][i])
                    sig_price_sell.append(np.nan)
                    flag = 1
                else:
                    sig_price_buy.append(np.nan)
                    sig_price_sell.append(np.nan)
            elif self.data_30day['Close'][i] < self.data_100day["Close"][i]:
                if flag != -1:
                    sig_price_buy.append(np.nan)
                    sig_price_sell.append(self.data[self.ticker][i])
                    flag = -1
                else:
                    sig_price_buy.append(np.nan)
                    sig_price_sell.append(np.nan)
            else:
                sig_price_buy.append(np.nan)
                sig_price_sell.append(np.nan)

        return (sig_price_buy, sig_price_sell)
