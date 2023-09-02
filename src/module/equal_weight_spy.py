"""Build an equal-weight (not market cap weight) SPY index"""

# https://www.youtube.com/watch?v=xfzGZB4HhEE&t=657s&ab_channel=freeCodeCamp.org

import pandas as pd
import numpy as np
import time
import datetime as dt

pd.options.mode.chained_assignment = None  # default='warn'

# an equal-weight SPY portfolio == a portfolio composed of equal amounts of each of the stocks in the SPY 500
# Our algorithm takes two inputs:
#   1. the given a portfolio size in $
#   2. the current SPY 500 stock tickers
# Our algorithm returns one output:
#   1. a dataframe with two columns
#   {
    # 'ticker': [] # a row for each SPY stock ticker
    # ,'shares': [] # the count of shares of each ticker to buy
# }
def calculate_equal_weight(portfolio:int, spy_stocks:str='assets/inputs/sp_list.csv', stock_prices:pd.DataFrame=None) -> pd.DataFrame:
    """Calculate the number of whole and part shares to buy of each stock on the S&P 500, given a portfolio value in dollars

    Generates a dataframe indicating the number of shares that should be purchased to yield an equal-weighted portfolio of the S&P 500 stocks.

    Args:
        portfolio (int): A dollar amount for which a S&P 500 purchase order should be generated.
        spy_stocks (str, optional): A filepath to a csv with one column containing the tickers of the S&P 500 stocks. Defaults to 'assets/inputs/sp_list.csv'.
        stock_prices (pd.DataFrame, optional): A dataframe of share prices for S&P 500 stocks. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    assert isinstance(portfolio, int), print(f'You entered {portfolio}. `portfolio` must be an integer.')
    assert isinstance(spy_stocks, str), print(f'You entered {spy_stocks}. `spy_stocks` must be a string to a csv of S&P 500 stock tickers.')
    assert isinstance(stock_prices, pd.DataFrame), print(f'`stock_prices` must be a pandas dataframe of S&P 500 stock prices.')
    
    start_time = time.time()

    spy_stocks = pd.read_csv(spy_stocks)
    portfolio_size = 10000 # portfolio value in $
    n_stocks = len(spy_stocks) # count of stocks to buy
    dollars_of_stock = portfolio_size/n_stocks # this is how much $ we need to buy of each stock
    # to calculate the number of shares to buy, we need the stock's current price divided by the stock's most-recent close price

    orders = pd.DataFrame({
        'ticker':[]
        ,'price':[]
        ,'buy_dollars':[]
        ,'buy_shares':[]
    })
    # time.strftime('%Y-%M-%d')
    orders['ticker'] = spy_stocks['Ticker']
    for i in range(len(orders['ticker'].unique())):
        ticker = orders['ticker'][i]
        mask = (stock_prices['ticker'] == ticker)
        max_date = max(stock_prices[mask]['date'])
        mask = (stock_prices['ticker'] == ticker) & (stock_prices['date']==max_date)
        tmp = stock_prices[mask]['close'].values[0]
        orders['price'][i] = tmp
        if i>0 and i % 25 == 0:
            print(f'completed {i} of {len(orders)} iterations ({round(((i)/len(orders)*100),2)}%)')
    print(f'Completed calculating buy shares for {len(spy_stocks)} tickers')
    orders['buy_dollars'] = dollars_of_stock
    orders['buy_shares_whole'] = np.ceil(orders['buy_dollars'] / orders['price'])
    orders['buy_shares_part'] = np.round(orders['buy_dollars'] / orders['price'], 2)

    end_time = time.time()
    elapsed = round(end_time-start_time, 2)
    
    print(f'Generated order sheet for {len(orders)} tickers')
    print(f'Elapsed time: {elapsed} s')

    return orders