from glob import glob
from importlib import import_module
import yfinance as yf
import pandas as pd
from progressbar import ProgressBar
# remove this later
from strategies import example

def run_all_learning(ticker):
    """Trains the bot with past data

    Arguments:
    ticker -- the ticker to get data on
    """
    filenames = glob("strategies/*.py")
    for x in range(len(filenames)):
        for filename in filenames:
            if "__init__.py" in filename:
                filenames.pop(x - 1)

    for filename in filenames:
        filename = filename.split("/")[1]
        filenames.append(filename.split(".")[0])
        filenames.pop(0)

    for strategy in filenames:
        import_module("strategies.{}".format(strategy)).Strategy(ticker)

def run_all(ticker):
    results = []
    return results

def incremental_data(limited_data):
    incremental = []
    for row in limited_data[:99]:
        incremental.append(row)
    for row in limited_data[99:]:
        incremental.append(row)
        yield incremental

def pause():
    input("Press enter to continue... ")

def correct_choice(current_value, future_data, buffer=0.02):
    future_average = future_data[:30].mean()
    #print(future_data[:30])
    #print("Current: {}  Future: {}".format(current_value, future_average))
    if current_value > future_average * (1 - buffer):
        # Stock goes down in future
        #print("Correct is Sell")
        return -1.0 # Sell
    elif current_value < future_average * (1 + buffer):
        # Stock goes up in future
        #print("Correct is Buy")
        return 1.0 # Buy
    else:
        # Stock didn't change much so hold is okay
        #print("Correct is Stay")
        return 0.0

def train(ticker, begin=-507, end=-251):
    ticker = yf.Ticker(ticker)
    score = 0
    # Gets all the past data up to a year ago
    data = ticker.history(period="max")[begin:end + 30]
    limited_data = data[:-30]
    data = data["Close"]
    limited_data = limited_data["Close"]
    # Offset because the data incremental starts with 100 days
    i = 99
    with ProgressBar(max_value=len(limited_data) - 99) as bar:
        for increment in incremental_data(limited_data):
            bar.update(i - 98)
            #increment is length 100 for some background data
            class_ = example.Strategy("AAPL", increment)
            result = class_.main()
            correct_action = correct_choice(increment[-1], data[i + 1:i + 31])
            if result == correct_action:
                score += 1.0
            elif result == 0.0:
                score += 1.0
            #print("-" * 32)
            i += 1

    print(score)
    score = round(score / (len(limited_data) - 99), 6)
    print("Final Score of: {}".format(score))

train("AAPL")
#example.Strategy("AAPL")
