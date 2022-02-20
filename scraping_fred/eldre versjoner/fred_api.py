import fredapi as fa
import pandas as pd
import os
from local_settings import fred as settings
import time

time_start = time.perf_counter()

FILE_PATH=(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_fred\\')

# get list of the full names (or most known as) of the fred symbols
def fred_list_name(i):
	fred_list_name = ["GDP_QUATERLY", "Currency_in_Circulation_WEEKLY"]
	return fred_list_name

# get list of fred symbols/acronyms
def fred_list():
	fred_list = ["GDP", "WCURCIR"]
	return fred_list

# get api acsess  with Fred api_key
def fred():
	fred = fa.Fred(settings['api_key'])
	return fred

def fred_scraper(fred_list):
	master_list=[]
	for i, acronyms in enumerate(fred_list()):
		data=fred().get_series(acronyms)
		master_list.append(data)
	return master_list

def main():
	fred_list()
	print(fred())
	print("_"*30)
	for i, acronyms in enumerate(fred_scraper(fred_list)):
		(pd.DataFrame(fred_scraper(fred_list)[i], columns=[fred_list()[i]])).to_csv(FILE_PATH+(fred_list_name(i)[i])+".csv", index=False, header=True)
		print(fred_list_name(i)[i]," was saved sucsessfully.")
		print("_"*50)
	return

if __name__ == '__main__':
	main()

time_elapsed = (time.perf_counter() - time_start)
print("Time elapsed in seconds: ",time_elapsed)






