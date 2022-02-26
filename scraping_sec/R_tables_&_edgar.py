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
import csv





#################################################################################################################################################################
#                                          ROUND 0: Prep work - import symbols & CIKs --> Merge & and drop non-matching symbols
#################################################################################################################################################################


'''
TO-DO: 
____________________________
(1) find CIK-list
(2) write code for merge-&-drop
 
(3) Finally: turn ROUNDs below into def-functions & make them run through new CIK-list 
____________________________
'''

DF = pd.read_csv(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_tickeR_LIST\CIK_list.csv')
# DF.set_index(DF['Symbol'], inplace=True)
CIK=DF['cik']
stock=DF['Symbol']
form_type=['10-k']

hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# pd.set_option('display.width', 200)
# pd.set_option('display.max_colwidth', 30)

base_url_sec='https://www.sec.gov/'

# hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
# R_LIST=pd.DataFrame(['R1','R2','R3','R4','R5','R6','R7','R8','R9'])
R_LIST=pd.DataFrame(['R6', 'R2'])
R1=pd.DataFrame(["R1"])

DOC_TABLE=None

# #################################################################################################################################################################
# #                                          ROUND 1: StartPunkt - from Edgar search --> list of company documents 
# #################################################################################################################################################################


def link_builder2():
	link_list=[]
	for i in CIK:
		link = base_url_sec+'cgi-bin/browse-edgar?action=getcompany&CIK='+str(i)+'&type='+form_type[0]+'&dateb=dt&owner=exclude&start=&output=&count=100'
		link_list.append(link)
		print
	return link_list


def request():
	doc_list=[]
	link_list = link_builder2()
	for link in link_list:
		req = requests.get(link, headers=hdr)
		content = req.content
		soup = BeautifulSoup(req.content, 'html.parser')
		doc_table = soup.find_all('table', class_='tableFile2')[0]
		doc_list.append(doc_table)
	return doc_list
	


def sec_navigator():
	global DOC_TABLE
	master_list = []
	if DOC_TABLE==None:
		DOC_TABLE=request()
	# print(doc_table)
	for table in DOC_TABLE:
		for row in table.find_all('tr')[0:2]:
		    
		    # find all the columns
		    cols = row.find_all('td')

		    # if there are no columns move on to the next row.
		    if len(cols) != 0:        
		        
		        # grab the text
		        filing_type = cols[0].text.strip()                 
		        filing_date = cols[3].text.strip()
		        filing_numb = cols[4].text.strip()
		        
		        # find the links
		        filing_doc_href = cols[1].find('a', {'href':True, 'id':'documentsbutton'})       
		        filing_int_href = cols[1].find('a', {'href':True, 'id':'interactiveDataBtn'})
		        filing_num_href = cols[4].find('a')
		        
		        # grab the the first href
		        if filing_doc_href != None:
		            filing_doc_link = base_url_sec + filing_doc_href['href'] 
		        else:
		            filing_doc_link = 'no link'
		        
		        # grab the second href
		        if filing_int_href != None:
		            filing_int_link = base_url_sec + filing_int_href['href'] 
		        else:
		            filing_int_link = 'no link'
		        
		        # grab the third href
		        if filing_num_href != None:
		            filing_num_link = base_url_sec + filing_num_href['href'] 
		        else:
		            filing_num_link = 'no link'


		        # create and store data in the dictionary
		        filing_date_short=filing_date[:-6]
		        file_dict = {}
		        file_dict['file_type'] = filing_type
		        file_dict['file_number'] = filing_numb
		        file_dict['file_date'] = filing_date
		        file_dict['filing_date_short']=filing_date_short
		        file_dict['links'] = {}
		        file_dict['links']['documents'] = filing_doc_link
		        file_dict['links']['interactive_data'] = filing_int_link
		        file_dict['links']['filing_number'] = filing_num_link

		    
		        ## let the user know it's working

		        # print('-'*100)        
		        # print("Filing Type: " + filing_type)
		        # print("Filing Date: " + filing_date)
		        # print("Filing Number: " + filing_numb)
		        # print("Document Link: " + filing_doc_link)
		        # print("Filing Number Link: " + filing_num_link)
		        # print("Interactive Data Link: " + filing_int_link)
		        
		        # append dictionary to master list
		        master_list.append(file_dict)
	df=pd.DataFrame(master_list)
	return df

#################################################################################################################################################################
#                                          ROUND 2: R_lsit --> Getting documents --> CSV
#################################################################################################################################################################



'''
R-TABLES CODE 
Kode for å laste ned bare tables fra "financial statements" 
+ droppe alle som som har "parenthetical" i seg
PLANEN: 
I "filing_int_link html" finner man en <li> som har en liste over alle R-tables 
som ligger i "Financial statements" med tittel. Plannen er å telle disse li'sene 
og bruke det som limiten på hvor R1-Rx skal stoppe, men den kan også brukes til å 
droppe de tittlene som inkluderer "parenthetical".
_________________________________________________________________________________
'''






def get_symbol(R1):
	symbol 	= DF.loc[DF['cik'] == int(R1)]
	print(symbol)
	return symbol['Symbol'].values.tolist()[0]

def get_accession_number(index):
	accession_number_list=[]
	df= sec_navigator()
	# print(df)
	df = df['links'][index]
	documents=df['interactive_data']
	parsed = urlparse(documents)
	query = parse_qs(parsed.query)
	[accession_number] = query['accession_number']
	accession_number = str(accession_number).replace("-", "")
	accession_number = int(accession_number)
	accession_number_list.append(accession_number)
	return accession_number




#GETTING R_LINKS:
def link_builder(cik,r, index):
	accession_number=get_accession_number(index)
	baselink= 'https://www.sec.gov'
	link_builder=baselink+"/Archives/edgar/data/"+str(cik)+"/"+str(accession_number).zfill(18)+"/"+r+".htm"

	return link_builder

#DATAFRAMING R_LINKS:
def R_links():
	r=pd.DataFrame(R_LIST)
	links=[]
	for i, cik in enumerate(CIK):
		for r_num in r[0]:
			links.append(link_builder(cik,r_num, i))
	l=pd.DataFrame(links)
	df = pd.concat([r, l], axis=1, ignore_index=True)
	df.columns =['doc_numb', 'R_link']
	return df

#GETTING THE TITLES:
def titles(i):
	req = requests.get(i ,headers=hdr)
	soup = BeautifulSoup(req.text, 'html.parser')
	doc_table = soup.find_all('table')
	
	title_list = []
	for row in doc_table[0].find_all('tr')[:1]:
		cols = row.find_all('th')
		file_dict = {}
		if len(cols) != 0:
			table_name = cols[0].text.strip()
			table_name_short	= table_name#[:-45]
			table_name_short	= table_name_short.replace(" ", "_")
			file_dict['table_name'] = table_name_short
			print("table_name:   " + table_name_short)
			for j in range(1,10):
				if j < len(cols):
					title  = cols[j].text.strip()
					print("title" + str(j) + ": " + title)
					file_dict['title'+str(j)] = title
				else:
					file_dict['title'+str(j)] = " "
		title_list.append(file_dict)
	return title_list



#GETTING THE TABLES:
def data(i):
	print(i)
	req = requests.get(i ,headers=hdr)
	soup = BeautifulSoup(req.text, 'html.parser')
	doc_table = soup.find_all('table')
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
		cols = row.find_all('td')
		file_dict = {}
		for j in range(1, 10):
			if j < len(cols):
				filing_text  = cols[j].text.strip()
				file_dict['filing_text'+str(j)] = filing_text
			else:
				file_dict['filing_text'+str(j)] = ' '
		master_list.append(file_dict)
	return master_list




def main():
	# pd.set_option('display.max_colwidth', None)
	pd.set_option('display.max_columns', None)
	pd.set_option('display.width', None)
	# pd.set_option('display.width', 200)
	# pd.set_option('display.max_colwidth', 10)
	request()
	R_link=list(R_links()['R_link'])	
	for i in (R_link):
	# for index, i in enumerate(R_link):

		df = pd.DataFrame(data(i))
		df2 =pd.DataFrame(titles(i))
		R=R_link
		cols = df.columns
		lencols = [ int(len(c)/2) for c in cols ]
		df.columns = pd.MultiIndex.from_tuples(tuple( ( c[:ln], c[ln:] ) for c, ln in zip(cols, lencols) ) )
		df["X"]=""
		df.insert(0, 'X', df.pop('X'))
		df. columns = df2.iloc[0]
		print("_"*80)
		cik=i[40:47]
		r_num=i[-6:-4]
		sec_nav   = sec_navigator()
		filing_date_short = sec_nav['filing_date_short'][0]
		form                = sec_nav['file_type'][0]
		# symbol              = (get_symbol(['symbol']))['symbol']
		print(cik)
		print(i)
		symbol              = get_symbol(cik)
		file_name=symbol+'_'+filing_date_short+'_'+form+'_'+str(r_num)
		file_path=r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_sec\10k\\'+file_name+'.csv'
		df.to_csv (file_path, index=False, header=True)
		print("_"*80)
		print("")
		print("Table has been sucsessfylly saved as: "+file_name)



if __name__ == '__main__':
	main()