# Directory code for CMD:
# cd documents/python/webScraping/nyse+nasdaq

#pip installs:
# pip install html5lib
# pip install BeautifulSoup4
# pip install schedule 


import pandas as pd
import numpy as np
import schedule
import time


df = pd.read_csv (r'~\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\tickerlist_nasdaq.csv')
df.drop(df.columns[2:12], axis=1, inplace=True)

# df['Name'] = df['Name'].str.replace('Inc.', '')
df['Name'] = df['Name'].str.replace('Common Stock', '')
df['Name'] = df['Name'].str.replace('Class A', '')
df['Name'] = df['Name'].str.replace('Class B', '')
df['Name'] = df['Name'].str.replace('Class C', '')


website='https://www.nyse.com/products/options-nyse-american-short-term'
df2 = pd.read_html(website)
df2=df2[0]
df2.columns=['Symbol', 'Name']


df = pd.concat([df, df2], ignore_index=True)
df.sort_values('Symbol', inplace=True, ignore_index=True)
df.drop_duplicates(subset='Symbol', keep="first", inplace=True)
# df.drop_duplicates(subset='Name', keep="first", inplace=True)
df.sort_values('Symbol', inplace=True, ignore_index=True)


# print("")
# print("JOINED LIST:")
# print("")
# print(df)

df.to_csv (r'~\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\tickerlist_nyse_nasdaq.csv', index = None, header=True) 

def nyse_list_update(t):

	website='https://www.nyse.com/products/options-nyse-american-short-term'
	global df
	df2 = pd.read_html(website)
	df2=df2[0]
	df2.columns=['Symbol', 'Name']
	print("NY OPTION LIST:")

	df = pd.concat([df, df2], ignore_index=True)
	df.sort_values('Symbol', inplace=True, ignore_index=True)
	df.drop_duplicates(subset='Symbol', keep="first", inplace=True)
	# df.drop_duplicates(subset='Name', keep="first", inplace=True)
	df.sort_values('Symbol', inplace=True, ignore_index=True)

	# print("")
	# print(" JOINED LIST:")
	# print("")
	# print(df)

	df.to_csv (r'~\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\tickerlist_nyse_nasdaq.csv', index = None, header=True) 

	return

schedule.every().day.at("20:30").do(nyse_list_update,'It is 20:30')

while True:
    schedule.run_pending()
    # time.sleep(60) # wait one minute

