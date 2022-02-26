import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import sys
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import datetime as dt
import os
import os.path
import json
from urllib.parse import urlparse, parse_qs

hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
stock = pd.read_csv(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\tickerlist_nyse_nasdaq.csv')
req = requests.get('https://www.sec.gov/include/ticker.txt' ,headers=hdr)
soup = BeautifulSoup(req.text)
soup = soup.find_all('p')[:1]
df = pd.read_table(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\cik.txt',header=None,sep='\t')
cik = pd.DataFrame(df)
s = pd.DataFrame(stock)
stock = pd.DataFrame(s['Symbol'])
stock = stock["Symbol"].str.lower() 
s.set_index(stock, inplace=True)
s=s["Symbol"].str.lower() 
cik.columns=['symbol', 'cik']
cik.set_index('symbol', inplace=True)
cik_list = pd.concat([s,cik],axis=1, ignore_index=False)
cik_list= cik_list.dropna()
m=(cik_list.dtypes=='float')
cik_list.loc[:,m]=cik_list.loc[:,m].astype(int)
cik_list.to_csv (r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\cik_list.csv', index=False, header=True)
print(cik_list)

