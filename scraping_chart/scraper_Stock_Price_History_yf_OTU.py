import time
import datetime
import pandas as pd
import yfinance as yf
from functools import cache


'''
___________________________________PURPOSE____________________________________

	ONE-TIME USAGE CODE, FOR GETTING ALL OF THE AVAILABLE PRICE HISTORY
______________________________________________________________________________

'''


'''
___________________________________TO-DO____________________________________

	- Implement Theading to this scraper
______________________________________________________________________________

'''


# SCRIPT TIMER (part 1):
time_start = time.perf_counter()

# DISABLING WARNING:
pd.options.mode.chained_assignment = None  # default='warn'

# FILE PATH:
FILE_PATH=r"C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_chart\\"


# VARIABLE LISTS
@cache
def variable_lists():
	# symbol_list=["A"]#, "AA", "AAPL", "TSLA"]	 #[PLACEHOLDER] [PLACEHOLDER] [PLACEHOLDER]
	# frequency=[('5d','1m')] 					 #[PLACEHOLDER] [PLACEHOLDER] [PLACEHOLDER]
	symbol_list= pd.read_csv(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_tickeR_LIST\tickerlist_nyse_nasdaq.csv')['Symbol']))
	frequency=[('5d','1m'),('1mo','5m'),('1mo','15m'),('1mo','1h'),('max','1d'),('max','1wk'),('max','1mo')]
	return symbol_list, frequency


# DOWNLOADER	
@cache
def downloader(t,p,i):
	data = yf.download(
	        # tickers list or string as well
	        tickers = t,

	        # use "period" instead of start/end
	        period = p,

	        # fetch data by interval (including intraday if period < 60 days)
	        interval = i,

	        # group by ticker (to access via data['SPY'])
	        group_by = 'ticker',

	        # adjust all OHLC automatically
	        auto_adjust = True,

	        # download pre/post regular market hours data
	        prepost = True,

	        # use threads for mass downloading? (True/False/Integer)
	        threads = True,

	        # proxy URL scheme use use when downloading?
	        proxy = None
	    )
	return data

# ALT 2 (saver & namer seperat):
def namer(t,p,i, data):
	return t+"_PriceChart_(p)"+p+"_(i)"+i+".csv"

def saver(file_name, FILE_PATH, data):
	return data.to_csv (FILE_PATH+file_name, index=True, header=True)


# MAIN
@cache
def main():
	print("STARTING SCRIPT..")
	print("="*20)
	symbol_list=variable_lists()[0]
	frequency=variable_lists()[1]
	for t in symbol_list:
		for p, i in frequency:
			data=downloader(t,p,i)
			file_name=namer(t,p,i, data)
			saver(file_name, FILE_PATH, data)
			print("sucessfully saved file: "+t+"_PriceChart_(p)"+p+"_(i)"+i+".csv")

if __name__ == '__main__':
	main()


# SCRIPT TIMER (part 2):
time_elapsed = (time.perf_counter() - time_start)
print("Time elapsed in seconds: ",time_elapsed)
