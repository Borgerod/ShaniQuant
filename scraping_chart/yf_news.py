import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import datetime as dt

# show news
def news(symbol, s):
	file_name=s+"_news.csv"
	return symbol.news.to_csv(path+"data_scraping_news"+X+file_name, index=False, header=True)


fn_list=[news]

path=(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_yf\\')

SYMBOL=['msft']#,'aapl', 'tsla']
# symbol_list= pd.read_csv(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_tickeR_LIST\tickerlist_nyse_nasdaq.csv')

def main():

	for i, s in enumerate(SYMBOL):
		print("saving "+s+"...")
		symbol = yf.Ticker(s)
		(fn_list[i % len(fn_list)])(symbol, s)
		print("-"*10)
		for i in fn_list:
			i(symbol, s)

if __name__ == '__main__':
	main()
