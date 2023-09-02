import pandas as pd
import numpy as np
import src.module.db as db
import src.module.equal_weight_spy as eqs
import sqlite3 as sq

# create a db, query price data for tickers, add data to db
# db.create_db('assets/inputs/trading.db')
# # tickers = ['SPY', 'GOOG']
# tickers = pd.read_csv('assets/inputs/sp_list.csv')
# tickers = tickers.Ticker.unique()
# tickers
# bars = db.pull_data(tickers=tickers, start="2001-01-01", end="2023-08-27")
# db.insert_data(df=bars, db='assets/inputs/trading.db')

con = sq.connect('assets/inputs/trading.db')
mydf = pd.read_sql_query("SELECT * from tbl_prices", con)
con.close()
mydf
mydf.columns
max(mydf['date'])

# test first strategy:
# the first strategy is to buy shares of each of the S&P 500 stocks
myorders = eqs.calculate_equal_weight(portfolio=100000, stock_prices=mydf)

# second strategy:
# quantitative momentum investing strategy

# third strategy:
# quantitative value strategy