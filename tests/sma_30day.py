# https://alpaca.markets/learn/technical-analysis-with-ta-lib-and-market-data-api/
# import market data via `alpaca_trade_api` and plot candlestick chart with 30-day simple moving average
import talib as ta
from alpaca_trade_api import REST, TimeFrame
import config
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
import numpy as np

rest_client = REST(config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
bars = rest_client.get_bars("SPY", TimeFrame.Day, "2021-06-01", "2021-10-01").df
bars['30_Day_SMA'] = ta.SMA(bars['close'], timeperiod=30) # calculate 30-day simple moving average
bars['upper_band'], bars['middle_band'], bars['lower_band'] = ta.BBANDS(bars['close'], timeperiod =30)
bars = bars.reset_index() # get rid of timestamp index

# Make a 30-day SMA fig
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

# Identify positions

def find_bband_positions(df:pd.DataFrame) -> pd.DataFrame:
    """Find positions given bollinger bands

    Args:
        df (pd.DataFrame): A dataframe of stock price data containing at least columns for upper and lower bands, and close prices.

    Returns:
        pd.DataFrame: The same dataframe as `df` but with one added column 'pos_type' indicating whether the position was identified as a 'buy' or 'sell'.
    """
    # initialize    
    bars['pos_type'] = 'none'
    # criteria
    # find points where the close was above the upper band; these may be points at which you'd want to sell the stock
    # find points where the close was below the lower band; these may be points at which you'd want to buy the stock

    # find sell positions
    mask = (bars['close'] > bars['upper_band'])
    bars['pos_type'] = np.where(mask, bars['pos_type'], 'sell')
    # find buy positions
    mask = (bars['close'] > bars['upper_band'])
    bars['pos_type'] = np.where(~mask, bars['pos_type'], 'buy')
    return bars

bars = find_bband_positions(bars)
bars

def find_volume_positions(df:pd.DataFrame) -> pd.DataFrame:
    pass
