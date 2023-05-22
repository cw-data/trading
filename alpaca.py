import config
import requests
import json
import talib as ta
from alpaca_trade_api import REST, TimeFrame
import config
import plotly.graph_objects as go
import plotly.express as px
import plotly.utils as pu
import json
import pandas as pd

ORDERS_URL = config.ALPACA_BASE_URL + '/v2/orders'
rest_client = REST(config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
bars = rest_client.get_bars("SPY", TimeFrame.Day, "2021-06-01", "2021-10-01").df
bars['simple_ma'] = ta.SMA(bars['close'], timeperiod=30)
bars['upper_band'], bars['middle_band'], bars['lower_band'] = ta.BBANDS(bars['close'], timeperiod=30)

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

def MainFig() -> str:
    """
    """
    # rest_client = REST(config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
    # bars = rest_client.get_bars("SPY", TimeFrame.Day, "2021-06-01", "2021-10-01").df
    # bars['30_Day_SMA'] = ta.SMA(bars['close'], timeperiod=30)
    # bars['upper_band'], bars['middle_band'], bars['lower_band'] = ta.BBANDS(bars['close'], timeperiod=30)
    candlestick_fig = go.Figure(data=[go.Candlestick(x=bars.index,
                    open=bars['open'],
                    high=bars['high'],
                    low=bars['low'],
                    close=bars['close'])])
    sma_fig = px.line(x=bars.index, y=bars['simple_ma'])
    upper_line_fig = px.line(x=bars.index, y=bars['upper_band'])
    lower_line_fig = px.line(x=bars.index, y=bars['lower_band'])
    fig = go.Figure(data=candlestick_fig.data + sma_fig.data + upper_line_fig.data + lower_line_fig.data)
    fig.update_layout(xaxis_rangeslider_visible=False, template='plotly_dark', showlegend=False)
    graphJSON = json.dumps(fig, cls=pu.PlotlyJSONEncoder)
    return graphJSON

def pos_table() -> str:
    # https://plotly.com/python/table/
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv').head()
    df = bars
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.open, df.high, df.low, df.close, df.volume, df.trade_count, df.vwap, df.simple_ma, df.upper_band, df.middle_band, df.lower_band],
                fill_color='lavender',
                align='left'))
    ])
    graphJSON = json.dumps(fig, cls=pu.PlotlyJSONEncoder)
    return graphJSON