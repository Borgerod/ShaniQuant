#############################################################################################################################
# MED JSON
#############################################################################################################################

import sys
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import datetime as dt
import os
import os.path

dt = datetime.today()
seconds = dt.timestamp()
df=""
headers = {
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1', # Do Not Track Request Header 
    'Connection'      : 'close'
    }

# # FOR TESTING: 
# symbol=['AAPL']
# stock=pd.DataFrame(symbol, columns = ['AAPL'])


#FOR USE: 
stock=pd.read_csv (r'~\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_ticker_list\tickerlist_nyse_nasdaq.csv')# encoding='utf-8')
stock=stock['Symbol']
# stock=stock[237:] #fortsettelse

for i in stock:
	link="https://query2.finance.yahoo.com/v7/finance/options/"+i
	# print(link)


	def option_request(i):
		req=requests.get(link, headers=headers).json()
		r=pd.DataFrame(req['optionChain']['result'])
		if r.empty:
			pass
			print("############# "+i+" REQUEST WAS PASSED IN: request         ##########  ")
		else:
			# print(r)
			return r



# QUOTES
	def Screener_op_quotes(i):
		# r=pd.json_normalize(r['quote'])
		file_name=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options\data_quotes.csv'
		r=pd.DataFrame(option_request(i))
		if "quote" not in r:
				print("############# "+i+" QUOTE WAS PASSED; did NOT have 'quote' ##########")
		else: 
			r=pd.DataFrame(r['quote'])
			r=pd.json_normalize(r['quote'][0])
			r['symbol'], col_name=i, 'symbol'
			r.insert(0, col_name, r.pop(col_name))
			if os.path.isfile(file_name):
				#IS PRESENT
				r = pd.concat([pd.read_csv (file_name), r], ignore_index=True)
				r.drop_duplicates(subset='symbol', keep="first", inplace=True)
				r.to_csv (file_name, index=False, header=True)
				print(i+" was ADDED to data_quotes.csv")
			else:
				#IS NOT PRESENT
				r.to_csv (file_name, index=False, header=True)
				print("NO FILE WAS FOUND; CREATED data_quotes.csv and ADDED "+i)
		return r



#OPTIONS
	def screener_options(i):
		path=r'~\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options'
		r=pd.DataFrame(option_request(i))
		if "options" not in r:
			print("###### "+i+" WAS PASSED in Options; 		did NOT have 'options' 			######")
			pass
		else:
			r=pd.DataFrame(r['options'])
			r=pd.json_normalize(r['options'][0])
			if "calls" not in r:
				print("###### "+i+" WAS PASSED in Options; 		did NOT have 'calls' 			######")
				pass
			elif "puts" not in r:
				print("###### "+i+" WAS PASSED in Options; 		did NOT have 'calls' 			######")
				pass
			else:
				return r


	def CALLS_DF(i):
		df=screener_options(i)
		df=pd.DataFrame(df)
		if "calls" not in df:
				print("###### "+i+" WAS PASSED in CALLS_DF; 	did NOT have 'calls' 			######")
		else:
			# print(i+" sucsess")
			df=pd.DataFrame(df['calls'][0])
			# df=df['calls'][0]
			if df.empty:
				print("###### "+i+" WAS PASSED in CALLS_DF;	 'calls' was empty				######")
			else:
				df.reset_index(drop=True, inplace=True)
				if "expiration" not in df:
					print("###### "+i+" WAS PASSED in CALLS_DF; 	no 'expiration' was found 		######  ")
				if "lastTradeDate" not in df:
					print("###### "+i+" WAS PASSED in CALLS_DF; 	no 'lastTradeDate' was found 	######  ")
				else:
					df['expiration'],df['lastTradeDate'] = pd.to_datetime(df['expiration'], unit='s').dt.date ,pd.to_datetime(df['lastTradeDate'], unit='s')
					df_op_calls=df

				
		 		#Checking if Files already exist
		 		#CSV_HISTORY:
					path=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options'
					file_name_two=path+"/"+i+"_calls_history.csv"
					if os.path.isfile(file_name_two):
						#IS PRESENT
						df_op_calls_gammel = pd.read_csv (file_name_two, delim_whitespace=True)
						if df_op_calls_gammel.empty:
							df_op_calls_gammel.to_csv (file_name_two, index=False, header=True)
							print(i+" calls HIST was saved.")
						else: 
							df_op_calls_gammel = pd.concat([df_op_calls_gammel, df_op_calls], ignore_index=True)
							df_op_calls.to_csv (file_name_two, index=False, header=True)
							print(i+" calls HIST was saved.")

					else: 
						#IS NOT PRESENT
						df_op_calls.to_csv (file_name_two, index=False, header=True)
						print(i+" calls HIST was saved.")
						return df_op_calls


					#CSV_TODAY:
					file_name=path+"/"+i+"_calls.csv"
					if os.path.isfile(file_name):
							#IS PRESENT
							df_op_calls_gammel = pd.read_csv (file_name, delim_whitespace=True)
							if df_op_calls_gammel.empty:
								df_op_calls.to_csv (file_name, index=False, header=True)
								print(i+" calls was saved.")
							else: 					
								df_op_calls_gammel = pd.concat([df_op_calls_gammel, df_op_calls], ignore_index=True)
								df_op_calls.to_csv (file_name, index=False, header=True)
								print(i+" calls was saved.")

					else: 
						#IS NOT PRESENT
						df_op_calls.to_csv (file_name, index=False, header=True)
						print(i+" calls was saved.")
						return df_op_calls


	def PUTS_DF(i):
			df=screener_options(i)
			df=pd.DataFrame(df)
			if "puts" not in df:
					print("###### "+i+" WAS PASSED in PUTS_DF; 	did NOT have 'puts' 			######")
			else:
				df=pd.DataFrame(df['puts'][0])
				if df.empty:
					print("###### "+i+" WAS PASSED in PUTS_DF;	 'puts' was empty				######")
				else:
					df.reset_index(drop=True, inplace=True)
					if "expiration" not in df:
						print("###### "+i+" WAS PASSED in PUTS_DF; 	no 'expiration' was found 		######  ")
					if "lastTradeDate" not in df:
						print("###### "+i+" WAS PASSED in PUTS_DF; 	no 'lastTradeDate' was found 	######  ")
					else:
						df['expiration'],df['lastTradeDate'] = pd.to_datetime(df['expiration'], unit='s').dt.date ,pd.to_datetime(df['lastTradeDate'], unit='s')
						df_op_puts=df


					#Checking if Files already exist
					#CSV_HISTORY:
					path=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options'
					file_name_two=path+"/"+i+"_puts_history.csv"
					if os.path.isfile(file_name_two):
						#IS PRESENT
						df_op_puts_gammel = pd.read_csv (file_name_two, delim_whitespace=True)
						if df_op_puts_gammel.empty:
							df_op_puts_gammel.to_csv (file_name_two, index=False, header=True)
							print(i+" puts HIST was saved.")
						else: 
							df_op_puts_gammel = pd.concat([df_op_puts_gammel, df_op_puts], ignore_index=True)
							df_op_puts.to_csv (file_name_two, index=False, header=True)
							print(i+" puts HIST was saved.")

					else: 
						# #IS NOT PRESENT
						df_op_puts.to_csv (file_name_two, index=False, header=True)
						print(i+" puts HIST was saved.")
						return df_op_puts

				#CSV_TODAY:
					file_name=path+"/"+i+"_puts.csv"
					if os.path.isfile(file_name):
							#IS PRESENT
							df_op_puts_gammel = pd.read_csv (file_name, delim_whitespace=True)
							if df_op_puts_gammel.empty:
								df_op_puts.to_csv (file_name, index=False, header=True)
								print(i+" puts was saved.")
							else: 					
								df_op_puts_gammel = pd.concat([df_op_puts_gammel, df_op_puts], ignore_index=True)
								df_op_puts.to_csv (file_name, index=False, header=True)
								print(i+" puts was saved.")
								
					else: 
						# #IS NOT PRESENT
						df_op_puts.to_csv (file_name, index=False, header=True)
						print(i+" puts was saved.")
						return df_op_puts


								## Alternativt: endre plassering på 'Contract Symbol'
								# if 'contractSymbol' in df_op_puts_gammel.iloc[:,0]:
								# 	# print("#############  SHOULD BE PASSED   ###############")
								# 	pass
								# else:		
								# 	column_numbers=[x for x in range(df_op_puts_gammel.shape[1])]
								# 	column_numbers.remove(0)
								# 	df_op_puts_gammel=df_op_puts_gammel.iloc[:, column_numbers] #return all columns except the 0th column

	def OPTIONS(i):
		CALLS_DF(i)
		PUTS_DF(i)

# FUNCTION CALLS
	# Screener_op_quotes(i)
	OPTIONS(i)






#VISUALISERING AV: 		QUOTE
def print_quotes():
	file_name=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options\data_quotes.csv'
	df_quote_old = pd.read_csv (file_name)
	df_quote_old.set_index('symbol', inplace=True)
	# pd.set_option('display.max_columns', None)
	# pd.set_option('display.width', 200)
	# print(df_quote_old.columns)
	print(df_quote_old)
	return df_quote_old


print_quotes()
