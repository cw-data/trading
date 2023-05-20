import config
import requests
import json

ORDERS_URL = config.ALPACA_BASE_URL + '/v2/orders'

def create_market_order(ticker, qty, side, type):
    data = {
        'symbol': ticker,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': 'gtc'
    }
    print(data)
    # r = requests.post(ORDERS_URL, json=data, headers=config.HEADERS)


class Order():
    def __init__(self) -> None:
        pass

    def place_order(self):
        r = requests.post(ORDERS_URL, json=self.data, headers=config.HEADERS)
        print('order placed')
        print(json.dumps(self.data, indent=4))
        print('---')
        print(r.content)
        # r = requests.post(ORDERS_URL, json=self.data, headers=config.HEADERS)


class MarketOrder(Order):
    def __init__(self, ticker:str, qty:int, side:str, type:str) -> None:
        self.ticker = ticker
        self.qty = qty
        self.side = side
        self.type = type
        self.data = {
            'symbol': self.ticker,
            'qty': self.qty,
            'side': self.side,
            'type': self.type,
            'time_in_force': 'gtc'
        }