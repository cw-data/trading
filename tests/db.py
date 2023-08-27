"""A routine for creating a trading database"""
import sqlite3 as sq
import talib as ta
from alpaca_trade_api import REST, TimeFrame
import config
import pandas as pd
import time
import numpy as np
import datetime as dt

# https://docs.python.org/3/library/sqlite3.html

def create_db(db_name:str) -> None:
    """Initialize an empty database

    Args:
        db_name (str): the filepath to the database
    """
    con = sq.connect(db_name)
    cur = con.cursor()
    qry = "DROP TABLE IF EXISTS tbl_prices"
    cur.execute(qry)
    qry = "CREATE TABLE tbl_prices(timestamp, open, high, low, close, volume, trade_count, vwap, date, ticker, sma_30, upper_band, middle_band, lower_band)"
    cur.execute(qry)
    
    print(f'Created `tbl_prices`:')
    qry = 'SELECT * FROM tbl_prices'
    result = cur.execute(qry)
    names = [description[0] for description in result.description]
    print(names)

    cur.close()

def pull_data(tickers:list, start:str="2021-06-01", end:str="2021-10-01") -> pd.DataFrame:
    """Pull data from the Alpaca API

    Args:
        tickers (list): A list of ticker symbols.
        start (str, optional): A date in YYYY-MM-DD format. The start of the date range for which you want data. Defaults to "2021-06-01".
        end (str, optional): A date in YYYY-MM-DD format. The end of the date range for which you want data. Defaults to "2021-10-01".

    Returns:
        pd.DataFrame: A dataframe of stock price information with bollinger bands and 30-day SMA calculated
    """
    start = time.time()
    print(f'Starting data collection for {len(tickers)} tickers...')

    data = pd.DataFrame({
        'timestamp': []
        ,'open': []
        ,'high': []
        ,'low': []
        ,'close': []
        ,'volume': []
        ,'trade_count': []
        ,'vwap': []
        ,'date': []
    })
    
    for i in range(len(tickers)):
        ticker = tickers[i]
        rest_client = REST(config.ALPACA_KEY_ID, config.ALPACA_SECRET_KEY)
        bars = rest_client.get_bars(ticker, TimeFrame.Day, start, end).df
        bars['ticker'] = ticker
        bars['sma_30'] = ta.SMA(bars['close'], timeperiod=30) # calculate 30-day simple moving average
        bars['upper_band'], bars['middle_band'], bars['lower_band'] = ta.BBANDS(bars['close'], timeperiod =30)
        bars = bars.reset_index() # get rid of timestamp index
        bars['date'] = bars['timestamp'].dt.date
        data = pd.concat([data, bars])
        print(f'Data collected for completed {ticker}: {i+1} of {len(tickers)} ({round(((i+1)/len(tickers)*100),2)}%)')
    
    end = time.time()
    elapsed = round(end-start, 2)
    
    print(f'Data collection completed for {len(tickers)} tickers')
    print(f'Elapsed time: {elapsed} s')
    
    return data

def insert_data(df:pd.DataFrame, db:str='trading.db') -> None:
    """Insert stock price data into database

    Args:
        df (pd.DataFrame): A dataframe of stock price data from `pull_data()`
    """
    if 'index' in df.columns:
        del df['index']
    print(f'Inserting {len(df)} rows into `tbl_prices`')
    con = sq.connect(db)
    df.to_sql('tbl_prices', con=con, if_exists='replace')
    con.commit()
    con.close()
    print(f'{len(df)} rows successfully inserted into `tbl_prices`')

# test
create_db('trading.db')
tickers = ['SPY', 'GOOG']
bars = pull_data(tickers)
insert_data(df=bars)

con = sq.connect('trading.db')
df = pd.read_sql_query("SELECT * from tbl_prices", con)
con.close()
df
