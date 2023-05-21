from flask import Blueprint, render_template, request
from alpaca import create_market_order, MarketOrder
import talib as ta
from alpaca_trade_api import REST, TimeFrame
import config
import plotly.graph_objects as go
import plotly.express as px
import plotly.utils as pu
import json
import pandas as pd

pages = Blueprint('pages', __name__)
rest_client = REST(config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)

@ pages.route('/', methods=['GET', 'POST'])
def index():

    rest_client = REST(config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
    bars = rest_client.get_bars("SPY", TimeFrame.Day, "2021-06-01", "2021-10-01").df
    bars['30_Day_SMA'] = ta.SMA(bars['close'], timeperiod=30)
    bars['upper_band'], bars['middle_band'], bars['lower_band'] = ta.BBANDS(bars['close'], timeperiod =30)
    candlestick_fig = go.Figure(data=[go.Candlestick(x=bars.index,
                    open=bars['open'],
                    high=bars['high'],
                    low=bars['low'],
                    close=bars['close'])])
    sma_fig = px.line(x=bars.index, y=bars['30_Day_SMA'])
    upper_line_fig = px.line(x=bars.index, y=bars['upper_band'])
    lower_line_fig = px.line(x=bars.index, y=bars['lower_band'])
    fig = go.Figure(data=candlestick_fig.data + sma_fig.data + upper_line_fig.data + lower_line_fig.data)
    fig.update_layout(xaxis_rangeslider_visible=False, template='plotly_dark', showlegend=False)
    graphJSON = json.dumps(fig, cls=pu.PlotlyJSONEncoder)

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        qty = request.form.get('qty')
        order_type = request.form.get('order_type')
        order_side = request.form.get('side')
        
        if order_type == 'market':
            order = MarketOrder(ticker, qty, order_side, order_type)
            print(order.data)
            order.place_order()
            return render_template('index.html', graphJSON=graphJSON)
        elif order_type == 'limit':
            return render_template('index.html', graphJSON=graphJSON)
        else:
            print("error: didn't match an order_type")

    return render_template('index.html', graphJSON=graphJSON)