

'''
R-TABLES CODE 
Kode for å laste ned bare tables fra "financial statements" 
+ droppe alle som som har "parenthetical" i seg

PLANEN: 
I "filing_int_link html" finner man en <li> som har en liste over alle R-tables 
som ligger i "Financial statements" med tittel. Plannen er å telle disse li'sene 
og bruke det som limiten på hvor R1-Rx skal stoppe, men den kan også brukes til å 
droppe de tittlene som inkluderer "parenthetical".

'''
# _________________________________________________________________________________



import requests

import pandas as pd
from bs4 import BeautifulSoup
import csv


hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
# R_list=pd.DataFrame(['R1','R2','R3','R4','R5','R6','R7','R8','R9'])
R_list=pd.DataFrame(['R6'])




#GETTING R_LINKS:
def link_builder(R_list):
	cik = 320193
	accession_number='000032019321000105'
	baselink= 'https://www.sec.gov'
	link_builder=baselink+"/Archives/edgar/data/"+str(cik)+"/"+str(accession_number)+"/"+R_list+".htm"
	
	# print(link_builder)
	return link_builder

#DATAFRAMING R_LINKS:
def R_links():
	r=pd.DataFrame(R_list)
	l=pd.DataFrame(link_builder(R_list))
	df = pd.concat([r, l], axis=1, ignore_index=True)
	df.columns =['doc_numb', 'R_link']
	return df

#GETTING THE TABLES:
def titles(i):
	# link=i
	req = requests.get(i ,headers=hdr)
	# print("Status for "+i+": ")
	# # print(req)
	# print("")
	soup = BeautifulSoup(req.text, 'html.parser')
	doc_table = soup.find_all('table')
	# print(soup.prettify)

	master_list = []
	#Finding titles:
	for row in doc_table[0].find_all('tr')[:1]:
		# find all the columns
		cols = row.find_all('th')#, class_='pl')
		# if there are no columns move on to the next row.
		file_dict = {}
		if len(cols) != 0:
			table_name = cols[0].text.strip()
			table_name_short	= table_name#[:-45]
			table_name_short	= table_name_short.replace(" ", "_")
			file_dict['table_name'] = table_name_short
			print("table_name:   " + table_name_short)
			for j in range(10):
				if j < len(cols):
					title  = cols[j].text.strip()
					print("title" + str(j) + ": " + title)
					file_dict['title'+str(j)] = title
				else:
					file_dict['title'+str(j)] = " "
		master_list.append(file_dict)




def data(i):
	# link=i
	req = requests.get(i ,headers=hdr)
	# print("Status for "+i+": ")
	# # print(req)
	# print("")
	soup = BeautifulSoup(req.text, 'html.parser')
	doc_table = soup.find_all('table')
	# master_list = []
	# print(soup.prettify)
	#Finding tables:
	master_list = []
	# file_dict = {'filing_text1': [],
	# 			'filing_text2': [],
	# 			'filing_text3':[],
	# 			'filing_text4':[],
	# 			'filing_text5':[],
	# 			'filing_text6':[],
	# 			'filing_text7':[],
	# 			'filing_text8':[],
	# 			'filing_text9':[]
	# 			}
	for row in doc_table[0].find_all('tr'):
		cols = row.find_all('td')#, class_='pl')
		file_dict = {}
		for j in range(1, 10):
			if j < len(cols):
				filing_text  = cols[j].text.strip()
				print("filing_text" + str(j) + ": " + filing_text)
				file_dict['filing_text'+str(j)] = filing_text
			else:
				file_dict['filing_text'+str(j)] = ' '
		master_list.append(file_dict)
	return master_list

	# titles(i)
# print(data(i))
def main():
	pd.set_option('display.max_colwidth', None)
	pd.set_option('display.max_columns', None)
	pd.set_option('display.width', None)
	pd.set_option('display.max_colwidth', 30)

	R_link=list(R_links()['R_link'])
	print(R_link)
	for i in R_link:
		df = pd.DataFrame(data(i))
		df.to_csv("df_csv.csv")
		print(df)


if __name__ == '__main__':
	main()