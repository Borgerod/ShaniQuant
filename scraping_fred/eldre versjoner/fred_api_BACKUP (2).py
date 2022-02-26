import fredapi as fa
import pandas as pd
import os
from local_settings import fred as settings

'''
ALTERNATIV MÅTE FOR API:
from config import fred
# payload = {'api_key': fred}
print(fred)
'''

FILE_PATH=(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_fred')

# get list of the full names (or most known as) of the fred symbols
def fred_list_name(i):
	fred_list_name = ["GDP_QUATERLY", "Currency_in_Circulation_WEEKLY"]
	return fred_list_name

# get list of fred symbols/acronyms
def fred_list():
	fred_list = ["gdp", "WCURCIR"]
	return fred_list

# get api acsess  with Fred api_key
def fred():
	fred = fa.Fred(settings['api_key'])
	return fred
# #_____________________________________________________________________________________________
# #FØRSTE ALTERNATIV TIL SCRAPER-SAVER:



# # function that iterates though fred_list to pull data 
# def fred_scraper(fred_list):
# 	master_list=[]
# 	for i, acronyms in enumerate(fred_list()):
# 		print("works")
# 		data=fred().get_series(acronyms)
# 		print(acronyms)
# 		print("")
# 		# print(lst[i])
# 		print(data)
# 		print("_"*30)
# 		master_list.append(data)
# 	return master_list
# 	return
# fred_scraper()

def fred_scraper(fred_list):
	master_list=[]
	for i, acronyms in enumerate(fred_list()):
		data=fred().get_series(acronyms)
		# print(acronyms)
		# print("")
		# # print(lst[i])
		# print(data)
		# print("_"*30)
		master_list.append(data)
	print(master_list)
	print("*"*50)
	return master_list
fred_scraper(fred_list)



def saver(fred_list):
	for i, acronyms in enumerate(fred_list()):
		print("works")
		# print(fred_list_name(i)[i]," was saved sucsessfully.")
		# (fred_list_name(i)[i]).to_csv(PATH+file_name, index=False, header=True)
	return
saver(fred_list)

def saver(fred_list):
	for i, acronyms in enumerate(fred_list()):
		print("works")
		# print(fred_list_name(i)[i]," was saved sucsessfully.")
		# (fred_list_name(i)[i]).to_csv(PATH+file_name, index=False, header=True)
	return 
saver(fred_list)




#_____________________________________________________________________________________________
#ANDRE ALTERNATIV TIL SCRAPER-SAVER:


# # function that iterates though fred_list to pull data 
# def fred_scraper(fred_list):
# 	for i, acronyms in enumerate(fred_list()):
# 		data=fred().get_series(acronyms)
# 		print(acronyms)
# 		print("")
# 		# print(lst[i])
# 		print(data)
# 		print("_"*30)
# 	return data


# def saver(data_list):
# 	for i, acronyms in enumerate(fred_list()):
# 		data.to_csv(PATH+file_name, index=False, header=True)
# 		print(acronyms)
# 		print("")
# 		# print(lst[i])
# 		print(gdp)
# 		print("_"*30)

# return freq7(i).to_csv (FILE_PATH+file_name, index=False, header=True)


#_____________________________________________________________________________________________

# def main():
# 	fred_list()
# 	print(fred())
# 	print("_"*30)
# 	fred_scraper(fred_list)

# if __name__ == '__main__':
# 	main()









