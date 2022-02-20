import fredapi as fa
import pandas as pd
import os
from local_settings import fred as settings
import time

time_start = time.perf_counter()

FILE_PATH=(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_fred\\')

# get list of the full names (or most known as) of the fred symbols
def fred_list_name():
	return ["GDP_QUATERLY", "Currency_in_Circulation_WEEKLY"]

# get list of fred symbols/acronyms
def fred_list():
	return ["GDP", "WCURCIR"]

# get api acsess  with Fred api_key
def fred():
	return fa.Fred(settings['api_key'])

# the scraper the main will iterate fred_list through
def fred_scraper(acronyms,f):
	print("scraping: ",acronyms)
	master_list=[]
	master_list.append(f.get_series(acronyms))
	return master_list

def main():
	print("running fred_scraper.py...")
	f=fred()
	fred_name=fred_list_name()
	for i, acronyms in enumerate(fred_list()):
		(pd.DataFrame(fred_scraper(acronyms,f),index=[acronyms]).transpose()).to_csv(FILE_PATH+(fred_name[i])+".csv", index=False, header=True)
	return

if __name__ == '__main__':
	main()

time_elapsed = (time.perf_counter() - time_start)
print("Time elapsed in seconds: ",time_elapsed)






