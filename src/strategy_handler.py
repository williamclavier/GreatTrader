from glob import glob
from importlib import import_module
import yfinance as yf
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from typing import Any, Union
from art import tprint


def run_all(ticker):
    print(ticker)
    results = []
    return results


def incremental_data(limited_data):
    incremental = []
    for row in limited_data[:99]:
        incremental.append(row)
    for row in limited_data[99:]:
        incremental.append(row)
        yield incremental


def incremental_all_data(data):
    incremental = [None, None]
    incremental[0] = data["Open"].tolist()[:99]
    incremental[1] = data["Close"].tolist()[:99]
    for i in range(100, len(data["Close"])):
        incremental[0].append(data["Open"][i])
        incremental[1].append(data["Close"][i])
        yield incremental[0], incremental[1]


def pause():
    input("Press enter to continue... ")


def correct_choice(current_value, future_data, buffer=0.05):
    future_average = future_data[:30].mean()
    # print(future_data[:30])
    # print("Current: {}  Future: {}".format(current_value, future_average))
    if current_value > future_average * (1 - buffer):
        # Stock goes down in future
        # print("Correct is Sell")
        return -1.0  # Sell
    elif current_value < future_average * (1 + buffer):
        # Stock goes up in future
        # print("Correct is Buy")
        return 1.0  # Buy
    else:
        # Stock didn't change much so hold is okay
        # print("Correct is Stay")
        return 0.0


def train_all(ticker, begin=-507, end=-251, output=False):
    """Trains the bot with past data

    Arguments:
    ticker -- the ticker to get data on
    """
    filenames = [filename.split("/")[1].split(".")[0] for filename in glob("strategies/*.py")]
    all_data = yf.Ticker(ticker).history(period="max", interval="1d")[begin:end + 30]
    all_data_limited = all_data[:-30]
    data = all_data["Close"]
    limited_data = data[:-30]
    scores = {}
    l_bar = '{desc}: {percentage:3.0f}%|'
    r_bar = '| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]'
    start_date = limited_data.index[0]
    end_date = limited_data.index[-1]

    for strategy in filenames:
        score = 0
        class_ = import_module("strategies.{}".format(strategy)).Strategy(ticker)
        if class_.incremental:
            i = 99
            for increment in tqdm(incremental_data(limited_data), bar_format='{l_bar}{bar}{r_bar}',
                                  total=(begin - end + 99) * -1, desc=class_.name + f" ({ticker})"):
                # Increment starts with 100 days of data for a background
                result = class_.main(increment)
                correct_action = correct_choice(increment[-1], data[i + 1:i + 31])
                if result == correct_action:
                    score += 1.0
                i += 1
        else:
            i = 99
            for open_, close in tqdm(incremental_all_data(all_data_limited), bar_format='{l_bar}{bar}{r_bar}',
                                     total=(begin - end + 100) * -1, desc=class_.name + f" ({ticker})"):
                result = class_.main(open_, close)
                correct_action = correct_choice(close[-1], data[i + 1:i + 31])
                if result == correct_action:
                    score += 1.0
                i += 1

        score = round(score / (len(limited_data) - 99), 6)
        scores[class_.name] = score

    # Store the data in a csv file
    data_folder: Union[Path, Any] = Path("data/")
    filename = data_folder / "StrategyAccuracies.csv"
    if filename.exists():
        file_data = pd.read_csv(filename, index_col=False)
        print(file_data)
    else:
        file_data = pd.DataFrame()
        file_data 
    # do processing here of the data
    # write the data to the csv file now
    file_data.to_csv(filename, index=False)

    if output:
        spaces = 19
        second_spaces = 13
        tprint(ticker)
        print("_" * 36)
        print("| Name:" + " " * 14 + "| Score: (%)  |")
        print("|" + "_" * 20 + "|" + "_" * 13 + "|")
        for key in scores:
            print("| {}{}| {}{}|".format(key, (spaces - len(key)) * " ", round(scores[key] * 100,4),
                                         (second_spaces - len(str(scores[key]))) * " "))
        print("|" + "_" * 20 + "|" + "_" * 13 + "|")
        print("From {}/{}/{} to {}/{}/{}".format(start_date.month, start_date.day, start_date.year, end_date.month,
                                                 end_date.day, end_date.year))
    else:
        return scores


"""def train(ticker, begin=-507, end=-251):
    score = 0
    # Gets all the past data up to a year ago
    tick = yf.Ticker(ticker)
    data = tick.history(period="max")[begin:end + 30]
    limited_data = data[:-30]
    data = data["Close"]
    limited_data = limited_data["Close"]
    # Offset because the data incremental starts with 100 days
    i = 99
    l_bar = '{desc}: {percentage:3.0f}%|'
    r_bar = '| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]'
    for increment in tqdm(incremental_data(limited_data), bar_format='{l_bar}{bar}{r_bar}', total=(begin-end+99)*-1):
        # Increment starts with 100 days of data for a background
        class_ = example.Strategy("AAPL")
        # class_ = stochastic_rsi.Strategy(tick, increment)
        result = class_.main(increment)
        correct_action = correct_choice(increment[-1], data[i + 1:i + 31])
        if result == correct_action:
            score += 1.0
        i += 1

    score = round(score / (len(limited_data) - 99), 6)
    print("Final Score of: {}".format(score))"""

train_all("AAPL")
"""ticker_list = ["GE", "BAC", "GPRO", "SPY", "GOOG", "AAPL", "TSLA"]
for tick in ticker_list:
    train_all(tick)"""
