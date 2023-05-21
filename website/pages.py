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

    if request.method == 'POST':
        
        ticker = request.form.get('ticker')
        qty = request.form.get('qty')
        order_type = request.form.get('order_type')
        order_side = request.form.get('side')
        # print(ticker)
        # print(qty)
        # print(order_type)

        # if order_type == 'Market':
        #     order = MarketOrder()
        if order_type == 'market':
            order = MarketOrder(ticker, qty, order_side, order_type)
            print(order.data)
            order.place_order()
            return render_template('index.html')
        elif order_type == 'limit':
            return render_template('index.html')
        else:
            print("error: didn't match an order_type")

    rest_client = REST(config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
    bars = rest_client.get_bars("SPY", TimeFrame.Day, "2021-06-01", "2021-10-01").df
    bars['30_Day_SMA'] = ta.SMA(bars['close'], timeperiod=30)
    candlestick_fig = go.Figure(data=[go.Candlestick(x=bars.index,
                    open=bars['open'],
                    high=bars['high'],
                    low=bars['low'],
                    close=bars['close'])])
    sma_fig = px.line(x=bars.index, y=bars['30_Day_SMA'])
    fig = go.Figure(data=candlestick_fig.data + sma_fig.data)
    graphJSON = json.dumps(fig, cls=pu.PlotlyJSONEncoder)
    # fig.show()
    # df = pd.DataFrame(
    #    {
    #         'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
    #         'Amount': [4, 1, 2, 2, 4, 5],
    #         'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
    #     }
    # )
    # fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')
    # graphJSON = json.dumps(fig, cls=pu.PlotlyJSONEncoder)
#    return render_template('notdash.html', graphJSON=graphJSON)

    return render_template('index.html', graphJSON=graphJSON)