import yfinance as yf
import pandas as pd
import os
import os.path
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mpl_dates
import datetime
from pandas.tseries.offsets import *
from datetime import date, timedelta
import time

time_start = time.perf_counter()


pd.options.mode.chained_assignment = None  # default='warn'


# PURPOSE: ONE-TIME USAGE CODE, FOR GETTING ALL OF THE AVAILABLE PRICE HISTORY



# FILE_PATH=r"C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_chart\\"
SYMBOL_LIST=["A", "AA", "AAPL", "TSLA"] # PLACEHOLDER
# # SYMBOL_LIST= pd.read_csv(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_tickeR_LIST\tickerlist_nyse_nasdaq.csv')['Symbol']

# Making dataframe: FREQUENZY 
PERIOD=["max", "max"]
INTERVAL=["1d", "1wk"]
FREQENZY=pd.concat([pd.DataFrame(PERIOD), pd.DataFrame(INTERVAL)], axis=1, ignore_index=True)
FREQENZY.columns =['period', 'interval']
FREQENZY=FREQENZY.T
# print(FREQENZY)

def downloader():
	data = yf.download(  # or pdr.get_data_yahoo(...
	        # tickers list or string as well
	        tickers = SYMBOL_LIST,

	        # use "period" instead of start/end
	        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
	        # (optional, default is '1mo')
	        period = PERIOD[0],

	        # fetch data by interval (including intraday if period < 60 days)
	        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
	        # (optional, default is '1d')
	        interval = INTERVAL[0],

	        # group by ticker (to access via data['SPY'])
	        # (optional, default is 'column')
	        group_by = 'ticker',

	        # adjust all OHLC automatically
	        # (optional, default is False)
	        auto_adjust = True,

	        # download pre/post regular market hours data
	        # (optional, default is False)
	        prepost = False,

	        # use threads for mass downloading? (True/False/Integer)
	        # (optional, default is True)
	        threads = True,

	        # proxy URL scheme use use when downloading?
	        # (optional, default is None)
	        proxy = None
	    )
	return data




def namer():
	for i in SYMBOL_LIST:
		ticker=i
		return ticker

# namer()




def splitter():
	data=downloader()
	for i in SYMBOL_LIST:
		ticker=i
		i=data[i]
		i['date'] = i.index
		# i.loc[row_indexer,col_indexer] = value
		i['weekday'] = i['date'].dt.dayofweek
		i['weekday_name'] = i['weekday'].apply(lambda w:(date(2021, 2, 1) + timedelta(days = w)).strftime('%A'))
		i=i.dropna()
		# print(ticker)
		print(i)
		return i

# splitter()


def saver():
	df=splitter()
	ticker=namer()
	file_name=ticker+"_PriceChart_(p)"+PERIOD[0]+"_(i)"+INTERVAL[0]+".csv"
	print(file_name)
# saver()







def main():
	for i, period in enumerate(FREQENZY):
	# for i in FREQENZY:
		print(i)
		print(period)
		# print(i)
		# print(period)
		# freq=i
		# print(freq['period'])
		# print(freq['interval'])
		return i


if __name__ == '__main__':
	main()



time_elapsed = (time.perf_counter() - time_start)
print("Time elapsed in seconds: ",time_elapsed)








# def downloader():
# 	for i in SYMBOL_LIST:
# 		def freq1(i):
# 			# (yf.download(tickers = i, period="5d", interval = "1m", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)
# 			return yf.download(tickers = i, period="5d", interval = "1m", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)
		

	# for i in SYMBOL_LIST:
	# 	def save1(i):
	# 		file_name=i+"_PriceHistory_(p)_5d_(i)_1m.csv"
	# 		print("save1 complete")
	# 		return freq1(i).to_csv (FILE_PATH+file_name, index=False, header=True)

	# 	save1(i)

