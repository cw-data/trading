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
df = rest_client.get_bars("SPY", TimeFrame.Day, "2021-06-01", "2021-10-01").df
df['sma_30'] = ta.SMA(df['close'], timeperiod=30) # calculate 30-day simple moving average
df['upper_band'], df['middle_band'], df['lower_band'] = ta.BBANDS(df['close'], timeperiod =30)
df = df.reset_index() # get rid of timestamp index
df['date'] = df['timestamp'].dt.date

# Make a 30-day SMA fig
df = mydf.copy()
mask = (df['ticker']=='GOOG')
df = df[mask]
df = df.tail()
candlestick_fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
sma_fig = px.line(x=df.index, y=df['sma_30'])
upper_line_fig = px.line(x=df.index, y=df['upper_band'])
lower_line_fig = px.line(x=df.index, y=df['lower_band'])
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
    df['pos_type'] = 'none'
    # criteria
    # find points where the close was above the upper band; these may be points at which you'd want to sell the stock
    # find points where the close was below the lower band; these may be points at which you'd want to buy the stock

    # find sell positions
    mask = (df['close'] > df['upper_band']) | (df['upper_band'] != np.NaN)
    df['pos_type'] = np.where(mask, df['pos_type'], 'sell')
    # find buy positions
    mask = (df['close'] < df['lower_band']) | (df['lower_band'].isnull()==False)
    df['pos_type'] = np.where(mask, df['pos_type'], 'buy')
    return df

df = find_bband_positions(df)
df



testdf = pd.DataFrame({
    'close': [10, 10, 10]
    ,'upper_band': [10, 11, 11]
    ,'lower_band': [9 ,9, 10]
})



print(df.to_string())

mytest = df[df['sma_30'].isna()]
mytest
def find_volume_positions(df:pd.DataFrame) -> pd.DataFrame:
    pass
