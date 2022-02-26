import yfinance as yf
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import datetime as dt
from pandas.tseries.offsets import *
from datetime import date, timedelta
import time
import concurrent.futures

'''
ERRROR NOTE:
AttributeError: 'NoneType' object has no attribute 'to_csv' på Calendar ACB
'''


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SCRIPT TIMER (part 1):
# time_start = time.perf_counter()
start=time.perf_counter()

X=(r'/')
PATH=(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_yf\\')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# # get name info
def info(sec):
	symbol=yf.Ticker(sec)
	df = pd.DataFrame.from_dict(symbol.info, orient='index', columns=["info"])
	category="info"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# # show actions (dividends, splits)
def actions(sec):
	symbol=yf.Ticker(sec)
	df=symbol.actions
	category="actions"
	print(f'{sec} is downloading {category}...')	
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show dividends
def dividends(sec):
	symbol=yf.Ticker(sec)
	df=symbol.dividends
	category="dividends"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# # show splits
def splits(sec):
	symbol=yf.Ticker(sec)
	df=symbol.splits
	category="splits"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show financials
def financials(sec):
	symbol=yf.Ticker(sec)
	df=symbol.financials
	category="financials"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

def Qfinancials(sec):
	symbol=yf.Ticker(sec)
	df=symbol.quaterly_financials
	category="quaterly_financials"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show major holders
def major_holders(sec):
	symbol=yf.Ticker(sec)
	df=symbol.major_holders
	category="major_holders"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show institutional holders
def institutional_holders(sec):
	symbol=yf.Ticker(sec)
	df=symbol.institutional_holders
	category="institutional_holders"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show balance sheet
def balance_sheet(sec):
	symbol=yf.Ticker(sec)
	df=symbol.balance_sheet
	category="balance_sheet"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

def Qbalance_sheet(sec):
	symbol=yf.Ticker(sec)
	df=symbol.quaterly_balance_sheet
	category="quaterly_balance_sheet"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show cashflow
def cashflow(sec):
	symbol=yf.Ticker(sec)
	df=symbol.cashflow
	category="cashflow"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

def Qcashflow(sec):
	symbol=yf.Ticker(sec)
	df=symbol.quarterly_cashflow
	category="quaterly_cashflow"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show earnings
def earnings(sec):
	symbol=yf.Ticker(sec)
	df=symbol.earnings
	category="earnings"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

def Qearnings(sec):
	symbol=yf.Ticker(sec)
	df=symbol.quaterly_earnings
	category="quaterly_earnings"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show sustainability
def sustainability(sec):
	symbol=yf.Ticker(sec)
	df=symbol.sustainability
	category="sustainability"
	print(f'{sec} is downloading {category}...')	
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

# show analysts recommendations
def recommendations(sec):
	symbol=yf.Ticker(sec)
	df=symbol.recommendations
	category="recommendations"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec
# show next event (earnings, etc)
def calendar(sec):
	symbol=yf.Ticker(sec)
	df=symbol.calendar
	category="calendar"
	print(f'{sec} is downloading {category}...')
	file_name=sec+"_"+category+".csv"
	df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
	return sec

def main():
	with concurrent.futures.ThreadPoolExecutor() as executer:
		secs=['msft','aapl','tsla']
		secs=pd.read_csv(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_tickeR_LIST\tickerlist_nyse_nasdaq.csv')
		secs=secs.drop(['Name'], axis=1)
		secs=list(secs['Symbol'])
		fn_list=[info, actions, dividends, splits, financials, major_holders, institutional_holders, balance_sheet, Qbalance_sheet, cashflow, Qcashflow, earnings, Qearnings, sustainability, recommendations, calendar]
		for i, func in enumerate(fn_list):
			results = executer.map(func, secs)

		for result in results:
			print(result)

if __name__ == '__main__':
	main()

finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s)')

