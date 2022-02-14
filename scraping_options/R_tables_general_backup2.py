

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
from collections import Counter 

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





# PRINTING MESSAGES & DF:
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

R_link=list(R_links()['R_link'])
# print("")
# print("_"*80)
# print('link_builder: sucsessfull')
# print("-"*25)
# print('R_links: sucsessfull')
# print("-"*25)
# print("_"*80)
# print("R_link DataFrame:")
# print(R_links())
# print("_"*80)
# print("")

pd.set_option('display.max_colwidth', 30)
# pd.set_option('display.max_columns', 5)
# pd.set_option('display.width', 100)





#GETTING THE TABLES:
for i in R_link:
	def titles(i):
		# link=i
		req = requests.get(i ,headers=hdr)
		# print("Status for "+i+": ")
		# # print(req)
		# print("")
		soup = BeautifulSoup(req.text, 'html.parser')
		doc_table = soup.find_all('table')
		master_list = []
		# print(soup.prettify)


		#Finding titles:
		for row in doc_table[0].find_all('tr')[:1]:

			# find all the columns
			cols = row.find_all('th')#, class_='pl')
			# if there are no columns move on to the next row.
			if len(cols) != 0:

				# grab the text
				# print('-'*100)
				file_dict = {}
				try:
					table_name = cols[0].text.strip()
					table_name_short	= table_name#[:-45]
					table_name_short	= table_name_short.replace(" ", "_")
					file_dict['table_name'] = table_name_short
					print("table_name:   " + table_name_short)

					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title1  = cols[1].text.strip()
					print("title1: " + title1)
					file_dict['title1'] = str(title1)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title2 = cols[2].text.strip()
					print("title2: " + title2)
					file_dict['title2'] = str(title2)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title3 = cols[3].text.strip()
					print("title3: " + title3)
					file_dict['title3'] = str(title3)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title4 = cols[4].text.strip()
					print("title4: " + title4)
					file_dict['title4'] = str(title4)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title5 = cols[5].text.strip()
					print("title5: " + title5)
					file_dict['title5'] = str(title5)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title6 = cols[6].text.strip()
					print("title6: " + title6)
					file_dict['title6'] = str(title6)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title7 = cols[7].text.strip()
					print("title7: " + title7)
					file_dict['title7'] = str(title7)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title8 = cols[8].text.strip()
					print("title8: " + title8)
					file_dict['title8'] = str(title8)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					title9 = cols[9].text.strip()
					print("title9: " + title9)
					file_dict['title9'] = str(title9)
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")


				# append to masterlist
				master_list.append(file_dict)
				print(master_list)
				# print(file_dict)


			# else: 
			# 	print(index, " doesn't exist")

master_list = []
for i in R_link:
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
		for row in doc_table[0].find_all('tr'):
		
			# find all the columns
			cols = row.find_all('td')#, class_='pl')

			# if there are no columns move on to the next row.
			if len(cols) != 0:
				file_dict = {}
				try:
					filing_text1  = cols[1].text.strip()
					print("filing_text1: " + filing_text1)
					file_dict['filing_text1'] = filing_text1
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					filing_text2 = cols[2].text.strip()
					print("filing_text2: " + filing_text2)
					file_dict['filing_text2'] = filing_text2
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					filing_text3 = cols[3].text.strip()
					print("filing_text3: " + filing_text3)
					file_dict['filing_text3'] = filing_text3
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					filing_text4 = cols[4].text.strip()
					print("filing_text4: " + filing_text4)
					file_dict['filing_text4'] = filing_text4
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					filing_text5 = cols[5].text.strip()
					print("filing_text5: " + filing_text5)
					file_dict['filing_text5'] = filing_text5
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					filing_text6 = cols[6].text.strip()
					print("filing_text6: " + filing_text6)
					file_dict['filing_text6'] = filing_text6
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					filing_text7 = cols[7].text.strip()
					print("filing_text7: " + filing_text7)
					file_dict['filing_text7'] = filing_text7
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					filing_text8 = cols[8].text.strip()
					print("filing_text8: " + filing_text8)
					file_dict['filing_text8'] = filing_text8
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")
				try:
					filing_text9 = cols[9].text.strip()
					print("filing_text9: " + filing_text9)
					file_dict['filing_text9'] = filing_text9
					# insert -->[COLUMN NAME CHANGE]
				except IndexError:
					print("Index doesn't exist!")

					#append to masterlist 
				master_list.append(file_dict)
				df=pd.DataFrame(master_list)

				# filing_date_short   = filing_date[:-6]
				# form                = df.at[2,'filing_text2'].replace("-", "")
				# symbol              = df.at[35,'filing_text2']
				# file_name=symbol+'_'+filing_date_short+'_'+form+'_'+table_name_short+'.csv'
				file_name='test.csv'
				df.to_csv (file_name, index=False, header=True)
				print("_"*80)
				print("")
				print("Table has been sucsessfylly saved as: "+file_name)

				return df

	# titles(i)
# print(data(i))
df=pd.DataFrame(data(i))
print(df)