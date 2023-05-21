# https://alpaca.markets/learn/technical-analysis-with-ta-lib-and-market-data-api/
# import market data via `alpaca_trade_api` and plot candlestick chart with 30-day simple moving average
import talib as ta
from alpaca_trade_api import REST, TimeFrame
import config
import plotly.graph_objects as go
import plotly.express as px

rest_client = REST(config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
bars = rest_client.get_bars("SPY", TimeFrame.Day, "2021-06-01", "2021-10-01").df

bars
bars['30_Day_SMA'] = ta.SMA(bars['close'], timeperiod=30) # calculate 30-day simple moving average
bars['upper_band'], bars['middle_band'], bars['lower_band'] = ta.BBANDS(bars['close'], timeperiod =30)
candlestick_fig = go.Figure(data=[go.Candlestick(x=bars.index,
                open=bars['open'],
                high=bars['high'],
                low=bars['low'],
                close=bars['close'])])
sma_fig = px.line(x=bars.index, y=bars['30_Day_SMA'])
upper_line_fig = px.line(x=bars.index, y=bars['upper_band'])
lower_line_fig = px.line(x=bars.index, y=bars['lower_band'])
# fig = go.Figure(data=candlestick_fig.data + sma_fig.data)
fig = go.Figure(data=candlestick_fig.data + sma_fig.data + upper_line_fig.data + lower_line_fig.data)
fig.show()



