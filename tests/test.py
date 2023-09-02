import pandas as pd
import numpy as np
import src.module.db as db
import sqlite3 as sq

# test
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
