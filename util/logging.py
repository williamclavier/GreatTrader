# Logs all the data for the program's actions
from util.stock import Price
from pathlib import Path
from datetime import datetime, date
import sqlite3 as sql

data_folder = Path("data/")


class Log:
    def __init__(self, name, virtual=True):
        self.name = name
        if virtual:
            self.filename = data_folder / "Virtual.db"
        else:
            self.filename = data_folder / "Real.db"
        self.createTable()

    def createTable(self):
        conn = sql.connect(self.filename)
        cursor = conn.cursor()
        try:
            cursor.execute('CREATE TABLE buy (date VARCHAR, \
                time VARCHAR, symbol VARCHAR, amount INT, \
                cost FLOAT)')
            conn.commit()
            cursor.execute('CREATE TABLE sell (date VARCHAR, \
                time VARCHAR, symbol VARCHAR, amount INT, \
                cost FLOAT)')
            conn.commit()
        except sql.OperationalError:
            pass
        conn.close()

    def Write(self, data, type):
        conn = sql.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO {0} (date, time, symbol, \
            amount, cost) VALUES (?,?,?,?,?)'.format(type),
            (data['date'], data['time'], data['symbol'], int(data['amount']),
                float(data['cost']))
        )
        conn.commit()
        conn.close()

    def Read(self, type):
        conn = sql.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM {}'.format(type))
        data = cursor.fetchall()
        return data

    def Buy(self, symbol, amount, date=date.today().strftime('%Y-%m-%d'),
            time=datetime.now().strftime('%H:%M:%S')):
        price = Price(symbol, amount)
        dataToWrite = {
            "date": date,
            "time": time,
            "symbol": symbol,
            "amount": amount,
            "cost": price
        }
        self.Write(dataToWrite, "buy")

    def Sell(
            self, symbol, amount, date=date.today().strftime('%Y-%m-%d'),
            time=datetime.now().strftime('%H:%M:%S')):
        price = Price(symbol, amount)
        dataToWrite = {
            "date": date,
            "time": time,
            "symbol": symbol,
            "amount": amount,
            "cost": price
        }
        self.Write(dataToWrite, "sell")
