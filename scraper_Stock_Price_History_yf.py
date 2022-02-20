import yfinance as yf
import pandas as pd
import os
import os.path



# PURPOSE: ONE-TIME USAGE CODE, FOR GETTING ALL OF THE AVAILABLE PRICE HISTORY



FILE_PATH=r"C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_chart\\"
SYMBOL_LIST=["A"] # PLACEHOLDER
# SYMBOL_LIST= pd.read_csv(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_tickeR_LIST\tickerlist_nyse_nasdaq.csv')['Symbol']

def downloader():
	for i in SYMBOL_LIST:
		def freq1(i):
			# (yf.download(tickers = i, period="5d", interval = "1m", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)
			return yf.download(tickers = i, period="5d", interval = "1m", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)
		
		def freq2(i):
			return yf.download(tickers = i, period="1mo", interval = "5m", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)

		def freq3(i):
			return yf.download(tickers = i, period="1mo", interval = "15m", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)
			
		def freq4(i):
			return yf.download(tickers = i, period="1mo", interval = "1h", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)
			
		def freq5(i):
			return yf.download(tickers = i, period="max", interval = "1d", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)
			
		def freq6(i):
			return yf.download(tickers = i, period="max", interval = "1wk", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)
			
		def freq7(i):
			return yf.download(tickers = i, period="max", interval = "1mo", group_by = "ticker", auto_adjust = True, prepost = True, threads = True, proxy = None)


	for i in SYMBOL_LIST:
		def save1(i):
			file_name=i+"_PriceHistory_(p)_5d_(i)_1m.csv"
			print("save1 complete")
			return freq1(i).to_csv (FILE_PATH+file_name, index=False, header=True)

		def save2(i):
			file_name=i+"_PriceHistory_(p)_1mo_(i)_5m.csv"
			print("save2 complete")
			return freq2(i).to_csv (FILE_PATH+file_name, index=False, header=True)	

		def save3(i):
			file_name=i+"_PriceHistory_(p)_1mo_(i)_15m.csv"
			print("save3 complete")
			return freq3(i).to_csv (FILE_PATH+file_name, index=False, header=True)

		def save4(i):
			file_name=i+"_PriceHistory_(p)_1mo_(i)_1h.csv"
			print("save4 complete")
			return freq4(i).to_csv (FILE_PATH+file_name, index=False, header=True)

		def save5(i):
			file_name=i+"_PriceHistory_(p)_max_(i)_1d.csv"
			print("save5 complete")
			return freq5(i).to_csv (FILE_PATH+file_name, index=False, header=True)

		def save6(i):
			file_name=i+"_PriceHistory_(p)_max_(i)_1wk.csv"
			print("save6 complete")
			return freq6(i).to_csv (FILE_PATH+file_name, index=False, header=True)

		def save7(i):
			file_name=i+"_PriceHistory_(p)_max_(i)_1mo.csv"
			print("save7 complete")
			return freq7(i).to_csv (FILE_PATH+file_name, index=False, header=True)

		save1(i),save2(i),save3(i),save4(i),save5(i),save6(i),save7(i)


def main():
	downloader()


if __name__ == '__main__':
	main()





