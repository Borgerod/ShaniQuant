import pandas as pd 
import requests 
from bs4 import BeautifulSoup
import warnings
from requests_html import HTMLSession
import re
from itertools import product


class Context:   
	def __init__(self):  
		self.current_dt=datetime.datetime.now()

#OPTIONS
pd.options.display.max_columns=4
# pd.options.display.max_rows=None
# pd.options.display.width=None
pd.set_option('display.width', 2000)

#disable warnings 
warnings.filterwarnings("ignore")

def ev_ebitda_request():
	s=HTMLSession()
	return s.get("https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/vebitda.html", verify=False)

def get_yahoo_names():
	file_path=(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\yahoo_finance_industries_list.csv')
	industry_list=pd.read_csv(file_path, names=['Industry_Name'])
	return industry_list

def old_ev_ebitda_byIndustry():
	r=ev_ebitda_request()
	table=r.html.find('table')[0]
	tabledata=[[c.text for c in row.find('td')] for row in table.find('tr')]
	df=pd.DataFrame(tabledata, columns=['Industry_Name', 'Number of firms', 'EV/EBITDAR&D', 'EV/EBITDA', 'EV/EBIT', 'EV/EBIT(1-t)','EV/EBITDAR&D_ALL', 'EV/EBITDA_ALL', 'EV/EBIT_ALL', 'EV/EBIT(1-t)_ALL'])
	df = df.iloc[2:,]
	# df.to_excel(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\ORIGINAL_INDUSTRIES.xlsx'))
	return df
	

def ev_ebitda_byIndustry():	
	df=old_ev_ebitda_byIndustry()
	df=df.reset_index(drop=True).iloc[:96,1:]
	new_names=pd.read_excel(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\Updated_Industry_Names.xlsx', names=['Industry_Name'])
	new_names = pd.Series(new_names.Industry_Name.values.flatten())
	df=pd.concat([new_names, df], axis=1)
	df.columns=['Industry_Name', 'Number_of_firms', 'EV/EBITDAR&D', 'EV/EBITDA', 'EV/EBIT', 'EV/EBIT(1-t)','EV/EBITDAR&D_ALL', 'EV/EBITDA_ALL', 'EV/EBIT_ALL', 'EV/EBIT(1-t)_ALL']
	return df

def MultiName_saver():
	file=ev_ebitda_byIndustry()
	return file.to_excel(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_first_analysis\MultiName_ev_ebitda_byIndustry.xlsx')
MultiName_saver()