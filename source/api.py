import requests


class AlphaVantageAPI:
    """
    Made to interface with the Alpha Vantage API to gather market data
    """
    def __init__(self):
        self.Key = self.getAPIKey()

    def getAPIKey(self, filename="API-Key"):
        """
        Opens the Alpha Vantage API-Key file to read the key in the file

        returns: API-Key as string
        """
        data = ""
        with open(filename, "rb") as APIKeyFile:
            for line in APIKeyFile:
                data += line.decode(encoding="UTF-8")
        if data == "":
            print("Please Enter in an API Key to the 'API-Key' file.")
            print("Visit https://www.alphavantage.co/support/#api-key")
            print("if you need a key.")
            exit()
        else:
            return data

    def getJSON(self, url, params):
        data = requests.get(url=url, params=params).json()
        return data

    def IntraDay(self, symbol, time="5min"):
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": time,
            "apikey": self.Key
        }
        return self.getJSON("https://www.alphavantage.co/query", params)
