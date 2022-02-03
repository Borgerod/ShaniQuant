
#############################################################################################################################
# MED JSON
#############################################################################################################################

import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

dt = datetime.today()
seconds = dt.timestamp()
stock="AAPL"
df=""
headers = {
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1', # Do Not Track Request Header 
    'Connection'      : 'close'
    }

link="https://query2.finance.yahoo.com/v7/finance/options/"+stock


def option_request(stock):
	r=requests.get(link, headers=headers).json()
	r=r['optionChain']
	r=r['result']
	df_op=pd.DataFrame(r)
	return df_op

def split_list(my_list, chunks):    
    return [my_list[i:i + chunks] for i in range(0, len(my_list), chunks)]


def Screener_op_quotes(stock):
	df_op=option_request(stock)
	# #QUOTES
	df_quote=df_op['quote']
	df_quote=pd.json_normalize(df_quote)
	df_quote.set_index('symbol', inplace=True)
	print(df_quote)
	return df_quote


def screener_op_expirationDates(stock):
	df_op=option_request(stock)
	# #EXPIRATION DATES
	r=df_op['expirationDates']
	ex_dates=list(r)

		#columns=exp_dates	
	ex_dates=pd.DataFrame(columns=ex_dates)
	print(ex_dates)

	# 	index=exp_dates
	# ex_dates=pd.DataFrame(index=ex_dates)
	# print(ex_dates)

	return ex_dates


def screener_options(stock):
	df_op=option_request(stock)
	# #OPTIONS
	df=df_op['options']
	df=list(df)


	#skal være under paraplyen "expirationDate"
	df=df[0]
	df=pd.json_normalize(df)
	df_op_ex=pd.to_datetime(df['expirationDate'], unit='s')
	# df_op_ex['expirationDate'] = pd.to_datetime(df['expirationDate'], format='%Y%m%d')
	df_op_ex=df_op_ex[0]
	df_op_ex=str(df_op_ex)


	#CALLS DF
	df_op_calls=df['calls']
	df_op_calls=df_op_calls[0]
	df_op_calls=pd.json_normalize(df_op_calls)
	# df_op_calls.style.set_caption('Put Options '+stock+", expirationDate: "+df_op_ex)
	index=df_op_calls.index
	index.name="CALL OPTIONS "+stock+" expirationDate: "+df_op_ex
	# pd.set_option("display.max_rows", None, "display.max_columns", None)

	df_op_calls['expiration'] = pd.to_datetime(df_op_calls['expiration'], unit='s')
	df_op_calls['lastTradeDate'] = pd.to_datetime(df_op_calls['lastTradeDate'], unit='s')
	print(df_op_calls)

	#PUTS DF
	df_op_puts=df['puts']
	df_op_puts=df_op_puts[0]
	df_op_puts=pd.json_normalize(df_op_puts)
	# df_op_puts.style.set_caption('Put Options '+stock+", expirationDate: "+df_op_ex)
	index=df_op_puts.index
	index.name="PUT OPTIONS "+stock+" expirationDate: "+df_op_ex
	# pd.set_option("display.max_rows", None, "display.max_columns", None)

	df_op_puts['expiration'] = pd.to_datetime(df_op_puts['expiration'], unit='s')
	df_op_puts['lastTradeDate'] = pd.to_datetime(df_op_puts['lastTradeDate'], unit='s')
	print(df_op_puts)

	return df_op_ex, df_op_puts, df_op_calls




Screener_op_quotes(stock)
screener_op_expirationDates(stock)
screener_options(stock)
