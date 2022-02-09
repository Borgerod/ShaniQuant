
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
stock=stock[289:] #fortsettelse

for i in stock:
	link="https://query2.finance.yahoo.com/v7/finance/options/"+i
	# print(link)


	def option_request(i):
		req=requests.get(link, headers=headers).json()
		r=pd.DataFrame(req['optionChain']['result'])
		if r.empty:
			pass
			print("############# "+i+" REQUEST WAS PASSED IN: request   ###############  ")
		else:
			# print(r)
			return r





# POTENSIELT SØPPEL
	# def option_request2(i):
	# 		r=option_request(i)
	# 		print("____----_____----____")
	# 		print(r)
	# 		print("____----_____----____")
	# 		# if r.empty:
	# 		# 	print("############# "+i+" REQUEST WAS PASSED IN: quotes   ###############  ")
	# 		# 	pass
	# 		# else:
	# 		# 	# print(q)
	# 		# 	q=q
	# 		# 	return q


		# r=r['optionChain']['result']
		# r=r['result']
		# print(df_op)
		# df_op_0=df_op[0]
# 		if df_op.empty:
# 			pass
# 			print("############# "+i+" REQUEST WAS PASSED IN: request   ###############  ")
# 		else:
# 			return df_op





# QUOTES
	def Screener_op_quotes(i):
		# r=pd.json_normalize(r['quote'])
		file_name=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options\data_quotes.csv'
		r=option_request(i)
		r=r['quote']
		if r.empty:
			print("############# "+i+" REQUEST WAS PASSED IN: quotes (r is Empty)  ###############  ")
			pass
		else:
			q=pd.json_normalize(r)
			# print(q)
			if q.empty:
				print("############# "+i+" REQUEST WAS PASSED IN: quotes (df-qoute is Empty)   ###############  ")
				pass
			else:
				col_name='symbol'
				# df_quote=pd.DataFrame(q)
				df_quote=q
				df_quote.insert(0, col_name, df_quote.pop(col_name))
				if os.path.isfile(file_name):
					# df_quote_old = pd.read_csv (file_name)
					df_quote = pd.concat([pd.read_csv (file_name), df_quote], ignore_index=True)
					df_quote.drop_duplicates(subset='symbol', keep="first", inplace=True)
					df_quote.to_csv (file_name, index=False, header=True)
					# print(df_quote)
					print(i+" was ADDED to data_quotes.csv")
				else:
					#IS NOT PRESENT
					df_quote.to_csv (file_name, index=False, header=True)
					print("NO FILE WAS FOUND; CREATED data_quotes.csv and ADDED "+i)
					# print(df_quote)
				return df_quote



#POTENSIELT SØPPEL
		# if r.empty:
		# 	print("############# "+i+" REQUEST WAS PASSED IN: quotes (r is Empty)  ###############  ")
		# 	pass
		# else:
		# df_quote, col_name = pd.json_normalize(option_request(i)['quote']),'symbol'
	
		col_name='symbol'
		df_quote=pd.DataFrame(q)
		if df_quote.empty:
			print("############# "+i+" REQUEST WAS PASSED IN: quotes (df-qoute is Empty)   ###############  ")
			pass
		else:
			df_quote.insert(0, col_name, df_quote.pop(col_name))
			if os.path.isfile(file_name):
				# df_quote_old = pd.read_csv (file_name)
				df_quote = pd.concat([pd.read_csv (file_name), df_quote], ignore_index=True)
				df_quote.drop_duplicates(subset='symbol', keep="first", inplace=True)
				df_quote.to_csv (file_name, index=False, header=True)
				print(i+" was ADDED to data_quotes.csv")
			else:
				#IS NOT PRESENT
				df_quote.to_csv (file_name, index=False, header=True)
				print("NO FILE WAS FOUND; CREATED data_quotes.csv and ADDED "+i)
			return df_quote







#OPTIONS
	def screener_options(i):
		path=r'~\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options'
		r=option_request(i)
		if r['options'] is None:
			pass
			print("############# "+i+" REQUEST WAS PASSED IN: options (r['options'] is Empty)  ###############  ")
		else:
			df=list(r['options'])
			df_exp=pd.json_normalize(df[0])
			# print(df_exp)
			if df_exp is None:
				pass
				print("############# "+i+" REQUEST WAS PASSED IN: options (df_exp is Empty)  ###############  ")
			return df_exp



	def CALLS_DF(i):
		# exp=expirationDate(i)
		df_exp=screener_options(i)
		# print(df_exp)
		print("_______________")
		if df_exp.empty:
			print("Empty")
			pass
		else:
			df_op_calls=df_exp["calls"]
			df_op_calls=pd.json_normalize(df_op_calls[0])
			df_op_calls.reset_index(drop=True, inplace=True)
			if df_op_calls.empty:
				pass
				print("############# "+i+" PUTS WAS PASSED (df_op_puts is empty) ###############  ")
			elif df_op_calls['expiration'].empty:
				pass
				print("############# "+i+" PUTS WAS PASSED (expiration is empty) ###############  ")
			else:
				df_op_calls['expiration'],df_op_calls['lastTradeDate'] = pd.to_datetime(df_op_calls['expiration'], unit='s').dt.date ,pd.to_datetime(df_op_calls['lastTradeDate'], unit='s')
				# print(i+" Sucsess")

# 		if df_exp is None:
# 			print("############# "+i+" CALLS_DF WAS PASSED IN: options (df_exp is Empty)  ############### ")
# 			pass
# 		else:
# 			df_op_calls=df_exp["calls"]
# 			df_op_calls=pd.json_normalize(df_op_calls[0])
# 			df_op_calls.reset_index(drop=True, inplace=True)
# 			# df_op_calls["expiration"]=df_op_calls["expiration"].dt.date
# 			# Litt usikker på dt.date om det er nødvendig 
# 		if df_op_calls.empty:
# 			pass
# 			print("############# "+i+" PUTS WAS PASSED (df_op_puts is empty) ###############  ")
# 		elif df_op_calls["expiration"].empty:
# 			pass
# 			print("############# "+i+" PUTS WAS PASSED (expiration is empty) ###############  ")
# 		else:
# 			df_op_calls["expiration"],df_op_calls["lastTradeDate"] = pd.to_datetime(df_op_calls["expiration"], unit='s').dt.date ,pd.to_datetime(df_op_calls["lastTradeDate"], unit='s')
# 			# df_op_puts["expiration"]=df_op_puts["expiration"].dt.date
# 			# Litt usikker på dt.date om det er nødvendig 


	# 		#Checking if Files already exist 
				path=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options'
				file_name_two=path+"/"+i+"_calls_history.csv"
				if os.path.isfile(file_name_two):
					if __name__ == '__main__':
						#IS PRESENT
						df_op_calls_gammel = pd.read_csv (file_name_two, delim_whitespace=True)
						if df_op_calls_gammel.empty:
							df_op_calls_gammel.to_csv (file_name, index=False, header=True)
							# print("NO FILE WAS FOUND; Saved "+i+"_calls_HISTORY.csv          for the first time")
							# print(df_op_calls)
							print(i+" was sucsessfully saved.")
						else: 
							df_op_calls_gammel = pd.concat([df_op_calls_gammel, df_op_calls], ignore_index=True)
							df_op_calls.to_csv (file_name_two, index=False, header=True)
							# print("Saved; "+i+"_calls_HISTORY.csv")
							if 'contractSymbol' in df_op_calls_gammel.iloc[:,0]:
								# print("#############  SHOULD BE PASSED   ###############")
								pass
							else:		
								column_numbers=[x for x in range(df_op_calls_gammel.shape[1])]
								column_numbers.remove(0)
								df_op_calls_gammel=df_op_calls_gammel.iloc[:, column_numbers] #return all columns except the 0th column
								# print(df_op_calls_gammel)
					else:
						#IS NOT PRESENT
						df_op_calls.to_csv (file_name_two, index=False, header=True)	
						# print("NO FILE WAS FOUND; Saved "+i+"_calls_HISTORY.csv for the first time")

					file_name=path+"/"+i+"_calls.csv"
					if os.path.isfile(file_name):
						if __name__ == '__main__':
							#IS PRESENT
							df_op_calls_gammel = pd.read_csv (file_name, delim_whitespace=True)
							if df_op_calls_gammel.empty:
								df_op_calls.to_csv (file_name, index=False, header=True)
								# print("NO FILE WAS FOUND; Saved "+i+"_calls.csv          for the first time")
								# print(df_op_calls)
								print(i+" was sucsessfully saved.")
							else: 					
								df_op_calls_gammel = pd.concat([df_op_calls_gammel, df_op_calls], ignore_index=True)
								df_op_calls.to_csv (file_name, index=False, header=True)
								# print("Saved; "+i+"_calls.csv")
								print(i+" was sucsessfully saved.")
								if 'contractSymbol' in df_op_calls_gammel.iloc[:,0]:
									# print("#############  SHOULD BE PASSED   ###############")
									pass
								else:		
									column_numbers=[x for x in range(df_op_calls_gammel.shape[1])]
									column_numbers.remove(0)
									df_op_calls_gammel=df_op_calls_gammel.iloc[:, column_numbers] #return all columns except the 0th column
					else: 
						# #IS NOT PRESENT
						df_op_calls.to_csv (file_name, index=False, header=True)
						# print("NO FILE WAS FOUND; Saved "+i+"_calls.csv          for the first time")
						# print(df_op_calls)
						print(i+" was sucsessfully saved.")
						return df_op_calls

	def PUTS_DF(i):
		# exp=expirationDate(i)
		df_exp=screener_options(i)
		# print(df_exp)
		if df_exp.empty:
			print("Empty")
			pass
		else:
			df_op_puts=df_exp["calls"]
			df_op_puts=pd.json_normalize(df_op_puts[0])
			df_op_puts.reset_index(drop=True, inplace=True)
			if df_op_puts.empty:
				pass
				print("############# "+i+" PUTS WAS PASSED (df_op_puts is empty) ###############  ")
			elif df_op_puts['expiration'].empty:
				pass
				print("############# "+i+" PUTS WAS PASSED (expiration is empty) ###############  ")
			else:
				df_op_puts['expiration'],df_op_puts['lastTradeDate'] = pd.to_datetime(df_op_puts['expiration'], unit='s').dt.date ,pd.to_datetime(df_op_puts['lastTradeDate'], unit='s')
				# print(i+" Sucsess")
# # 		# exp=expirationDate(i)
# 		df_exp=screener_options(i)
# 		if df_exp is None:
# 			print("############# "+i+" PUTS_DF WAS PASSED IN: options (df_exp is Empty)  ############### ")
# 			pass
# 		else:
# 			df_op_puts=df_exp['puts']
# 			df_op_puts=pd.json_normalize(df_op_puts[0])
# 			df_op_puts.reset_index(drop=True, inplace=True)
# 			if df_op_puts.empty:
# 				pass
# 				print("############# "+i+" PUTS WAS PASSED (df_op_puts is empty) ###############  ")
# 			elif df_op_puts["expiration"].empty:
# 				pass
# 				print("############# "+i+" PUTS WAS PASSED (expiration is empty) ###############  ")
# 			else:
# 				df_op_puts["expiration"],df_op_puts["lastTradeDate"] = pd.to_datetime(df_op_puts["expiration"], unit='s').dt.date ,pd.to_datetime(df_op_puts["lastTradeDate"], unit='s')
# 				# df_op_puts["expiration"]=df_op_puts["expiration"].dt.date
# 				#Litt usikker på dt.date om det er nødvendig 


		

		#Checking if Files already exist 
				path=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options'
				file_name_two=path+"/"+i+"_puts_history.csv"
				if os.path.isfile(file_name_two):
					if __name__ == '__main__':
						df_op_puts_gammel = pd.read_csv (file_name_two, delim_whitespace=True)
						if df_op_puts_gammel.empty:
							df_op_puts.to_csv (file_name_two, index=False, header=True)
							# print("NO FILE WAS FOUND; Saved "+i+"_puts_HISTORY.csv          for the first time")
							print(i+" was sucsessfully saved.")
						else:
							df_op_puts_gammel = pd.concat([df_op_puts_gammel, df_op_puts], ignore_index=True)
							df_op_puts.to_csv (file_name_two, index=False, header=True)
							# print("Saved; "+i+"_puts_HISTORY.csv")
							if 'contractSymbol' in df_op_puts_gammel.iloc[:,0]:
								# print("#############  SHOULD BE PASSED   ###############")
								pass
							else:		
								column_numbers=[x for x in range(df_op_puts_gammel.shape[1])]
								column_numbers.remove(0)
								df_op_puts_gammel=df_op_puts_gammel.iloc[:, column_numbers] #return all columns except the 0th column
								# print(df_op_puts_gammel)
					else:
						df_op_puts.to_csv (file_name_two, index=False, header=True)	
						# print("NO FILE WAS FOUND; Saved "+i+"_puts_HISTORY.csv for the first time")

					file_name=path+"/"+i+"_puts.csv"
					if os.path.isfile(file_name):
						if __name__ == '__main__':
							df_op_puts_gammel = pd.read_csv (file_name, delim_whitespace=True)
							if df_op_puts_gammel.empty:
								df_op_puts.to_csv (file_name_two, index=False, header=True)
								# print("NO FILE WAS FOUND; Saved "+i+"_puts.csv          for the first time")
								print(i+" was sucsessfully saved.")
							else:
								df_op_puts_gammel = pd.concat([df_op_puts_gammel, df_op_puts], ignore_index=True)
								df_op_puts.to_csv (file_name, index=False, header=True)
								# print("Saved; "+i+"_puts.csv")
								if 'contractSymbol' in df_op_puts_gammel.iloc[:,0]:
									# print("#############  SHOULD BE PASSED   ###############")
									pass
								else:		
									column_numbers=[x for x in range(df_op_puts_gammel.shape[1])]
									column_numbers.remove(0)
									df_op_puts_gammel=df_op_puts_gammel.iloc[:, column_numbers] #return all columns except the 0th column
					else: 
						df_op_puts.to_csv (file_name, index=False, header=True)
						# print("NO FILE WAS FOUND; Saved "+i+"_puts.csv          for the first time")
						# print(df_op_puts)
						return df_op_puts

	def OPTIONS(i):
		CALLS_DF(i)
		PUTS_DF(i)

# # FUNCTION CALLS
	Screener_op_quotes(i)
	# OPTIONS(i)
	# CALLS_DF(i)
	

# #VISUALISERING AV: 		QUOTE
# def print_quotes():
# 	file_name=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options\data_quotes.csv'
# 	df_quote_old = pd.read_csv (file_name)
# 	df_quote_old.set_index('symbol', inplace=True)
# 	# pd.set_option('display.max_columns', None)
# 	# pd.set_option('display.width', 200)
# 	# print(df_quote_old.columns)
# 	print(df_quote_old)
# 	return df_quote_old


# print_quotes()