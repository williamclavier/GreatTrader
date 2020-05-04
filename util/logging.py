# Logs all the data for the program's actions
import util.stock
from pathlib import Path
from datetime import datetime, date
import sqlite3 as sql

data_folder = Path("data/")


class Log:
    def __init__(self, virtual=True):
        if virtual:
            self.filename = data_folder / "Virtual.db"
        else:
            self.filename = data_folder / "Real.db"
        self.create_table()

    def create_table(self):
        try:
            conn = sql.connect(self.filename)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE buy (date VARCHAR, \
                time VARCHAR, symbol VARCHAR, amount INT, \
                cost FLOAT)")
            conn.commit()
            cursor.execute('CREATE TABLE sell (date VARCHAR, \
                time VARCHAR, symbol VARCHAR, amount INT, \
                cost FLOAT)')
            conn.commit()
            conn.close()
        # if the table already exists just move on
        except sql.OperationalError:
            pass

    def write(self, data, action_type):
        conn = sql.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO {0} ("date", time, symbol, \
            amount, cost) VALUES (?,?,?,?,?)'.format(action_type),
            (data['date'], data['time'], data['symbol'], int(data['amount']),
                float(data['cost']))
        )
        conn.commit()
        conn.close()

    def read(self, action_type):
        conn = sql.connect(self.filename)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM {}'.format(action_type))
        data = cursor.fetchall()
        return data

    def buy(self, symbol, amount, current_date=date.today().strftime('%Y-%m-%d'),
            time=datetime.now().strftime('%H:%M:%S')):
        price = util.stock.price(symbol, amount)
        data_to_write = {
            "date": current_date,
            "time": time,
            "symbol": symbol,
            "amount": amount,
            "cost": price
        }
        self.write(data_to_write, "buy")

    def sell(
            self, symbol, amount, current_date=date.today().strftime('%Y-%m-%d'),
            time=datetime.now().strftime('%H:%M:%S')):
        price = util.stock.price(symbol, amount)
        data_to_write = {
            "date": current_date,
            "time": time,
            "symbol": symbol,
            "amount": amount,
            "cost": price
        }
        self.write(data_to_write, "sell")
