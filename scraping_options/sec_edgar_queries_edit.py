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

#test




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


























#################################################################################################################################################################
#                                          ROUND 1: StartPunkt - from Edgar search --> list of company documents 
#################################################################################################################################################################


'''
TO-DO: 
____________________________

(1) link: format baselink from CIk-list & other param. 




____________________________

'''

# Example of how to do TO-DO (1) [needs to be changed]
# ____________________________________________________________________________________________________________________________________
# start = 2019
# end = 2022
# cik_input = 1090872
# # cik= cik.zfill(10)
# cik=220000000000+cik_input
# short_cik = str(cik)[-6:] #we will need it later to form urls

# import requests
# from bs4 import BeautifulSoup as bs 
# url = f'https://www.sec.gov/cgi-bin/srch-edgar?text=cik%3D%{cik}%22+AND+form-type%3D(10-q*+OR+10-k*)&first={start}&last={end}'
# req = requests.get(url)
# print(req.url)
# soup = bs(req.text,'lxml')
# ____________________________________________________________________________________________________________________________________




link = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1090872&type=10-k&dateb=dt&owner=exclude&start=&output=&count=100'


# def get_data(link):
hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}
req = requests.get(link,headers=hdr)

# print('-'*50)
# print("LINKS: ")
# print("")
# print("Startlink from ROUND 1: "+link)
# print("Status Code: ")
# print(req.status_code)
# print("------------")
# print("")

content = req.content
# return content
# data = get_data(test_URL)

soup = BeautifulSoup(req.content, 'html.parser')
doc_table = soup.find_all('table', class_='tableFile2')
# define a base url that will be used for link building.
base_url_sec = r"https://www.sec.gov"
# print(soup.prettify)

master_list = []

for row in doc_table[0].find_all('tr')[0:3]:
    
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
        file_dict = {}
        file_dict['file_type'] = filing_type
        file_dict['file_number'] = filing_numb
        file_dict['file_date'] = filing_date
        file_dict['links'] = {}
        file_dict['links']['documents'] = filing_doc_link
        file_dict['links']['interactive_data'] = filing_int_link
        file_dict['links']['filing_number'] = filing_num_link
    
        ## let the user know it's working
        print('-'*100)        
        print("Filing Type: " + filing_type)
        print("Filing Date: " + filing_date)
        print("Filing Number: " + filing_numb)
        print("Document Link: " + filing_doc_link)
        print("Filing Number Link: " + filing_num_link)
        print("Interactive Data Link: " + filing_int_link)
        
        # append dictionary to master list
        master_list.append(file_dict)


# ***
# ## Section Three: Parsing the Master List
# We the `master_list` now populated we can iterate through the dictionary 
# in the list and grab the values we want from each dictionary by passing the keys
#  corresponding to that value. In the example below, I want all the links from a given
#   dictionary, so I parse the links dictionary.

# In[64]:


# loop through to get the links from the dictionary
# for report in master_list[0:2]:
    
    # print('-'*100)
    # print(report['links']['documents'])
    # print(report['links']['filing_number'])
    # print(report['links']['interactive_data'])





















    
#################################################################################################################################################################
#                                          ROUND 2: Navigate: From list of company documents --> Specific document-file
#################################################################################################################################################################


'''
TO-DO: 
____________________________
(1)




____________________________

'''




'''
CUTOUT OF HTML; ONLY FOR REFERANCE
_____________________________________________________________________________________________________________________________________________________________________________________________________________________
From ROUND 2's site 

#                 <tr>
#             0       <td scope="row">1</td>
#             1       <td scope="row">10-K</td>
#             2       <td scope="row"><a href="/ix?doc=/Archives/edgar/data/1090872/000109087221000027/a-20211031.htm">a-20211031.htm</a>   <span style="color: green">iXBRL</span></td>
#             3       <td scope="row">10-K</td>
#             4       <td scope="row">4539259</td>
#                 </tr>

From ROUND 1's site 
                    # <tr>
                    # <td nowrap="nowrap">10-K</td>
                    # <td nowrap="nowrap"><a href="/Archives/edgar/data/1090872/000109087221000027/0001090872-21-000027-index.htm" id="documentsbutton"> Documents</a>  <a href="/cgi-bin/viewer?action=view&amp;cik=1090872&amp;accession_number=0001090872-21-000027&amp;xbrl_type=v" id="interactiveDataBtn"> Interactive Data</a></td>
                    # <td class="small">Annual report [Section 13 and 15(d), not S-K Item 405]<br/>Acc-no: 0001090872-21-000027 (34 Act)  Size: 22 MB             </td>
                    # <td>2021-12-17</td>
                    # <td nowrap="nowrap"><a href="/cgi-bin/browse-edgar?action=getcompany&amp;filenum=001-15405&amp;owner=exclude&amp;count=100">001-15405</a><br/>211502413         </td>
                    # </tr>
_____________________________________________________________________________________________________________________________________________________________________________________________________________________
'''

# Filen jeg vil ha:   0001090872-21-000027.txt

second_link=filing_doc_link
# second_link='https://www.sec.gov/Archives/edgar/data/1090872/000109087221000027/0001090872-21-000027-index.htm'
req = requests.get(second_link,headers=hdr)
# print("Startlink from ROUND 2: "+filing_doc_link)
# print("")
# print("Status Code: ")
# print(req.status_code)
# print("------------")
# print("")
soup = BeautifulSoup(req.content, 'html.parser')
doc_table = soup.find_all('table', class_ ='tableFile')
master_list = []




for row in doc_table[0].find_all('tr')[9:10]:
    
    # find all the columns
    cols = row.find_all('td')

        # if there are no columns move on to the next row.
    if len(cols) != 0:        
        
        # grab the text
        # filing_type = cols[1].text.strip()
        # filing_date = cols[3].text.strip()
        filing_numb2 = cols[2].text.strip()
        
        # find the links
        filing_doc_href = cols[2].find('a', {'href':True})       #, 'id':'documentsbutton'})
        # filing_int_href = cols[1].find('a', {'href':True, 'id':'interactiveDataBtn'})
        filing_num_href = cols[2].find('a')

        for row in doc_table[0].find_all('tr')[1:2]:
            cols = row.find_all('td')
            if len(cols) != 0:
                filing_type = cols[1].text.strip()

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
        file_dict = {}
        file_dict['file_type'] = filing_type
        file_dict['file_number'] = filing_numb2
        file_dict['file_date'] = filing_date
        file_dict['links'] = {}
        file_dict['links']['documents'] = filing_doc_link
        file_dict['links']['interactive_data'] = filing_int_link
        file_dict['links']['filing_number'] = filing_num_link
    
        # # let the user know it's working
        print('-'*100)        
        print("Filing Type: " + filing_type)
        print("Filing Date: " + filing_date)
        print("Filing Number: " + filing_numb2)
        print("Document Link: " + filing_doc_link)
        print("Filing Number Link: " + filing_num_link)
        print("Interactive Data Link: " + filing_int_link)
        
        # append dictionary to master list
        master_list.append(file_dict)






















#################################################################################################################################################################
#                                          ROUND 3: Grab Document: From specific document-file --> Find all elements you want to download 
#################################################################################################################################################################


'''
TO-DO: 
____________________________
(1)




____________________________

'''
#If you want Interactive
# third_link=filing_int_link 
# print(filing_int_link)

# a 2020
# third_link='https://www.sec.gov/cgi-bin/viewer?action=view&cik=1090872&accession_number=0001090872-20-000020&xbrl_type=v'

# a 2021
# third_link='https://www.sec.gov/cgi-bin/viewer?action=view&cik=1090872&accession_number=0001090872-21-000027&xbrl_type=v'

# aapl 2021
third_link='https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-21-000105&xbrl_type=v'

req = requests.get(third_link,headers=hdr)

print("Startlink from ROUND 3: "+filing_int_link)
print("")
print("Status Code: ")
print(req.status_code)
print("")
print('-'*50)

soup = BeautifulSoup(req.content, 'html.parser')



# #If you want TXT
# third_link=filing_doc_link 
# print("Startlink from ROUND 3: "+filing_doc_link)
# print("")
# req = requests.get(third_link,headers=hdr)
# print("Status Code: ")
# print(req.status_code)
# print("")
# print('-'*50)

# soup = BeautifulSoup(req.content, 'html.parser')
# # print(soup.prettify)
# stat_operations = soup.find_all('table', id ='idm139639486070472')
# # stat_income = soup.find_all('table', id ='idm139639486972888')
# # balance_sheet = soup.find_all('table', id ='idm139639491907368')
# # stat_cashflow = soup.find_all('table', id ='idm139639492530216')
# # stat_equity = soup.find_all('table', id ='idm139639704543944')
# master_list = []



# # TRY NR. 1 
# # Grab each single element from TXT-file, based on previous code: 
# # ____________________________________________________________________________________________________________

# '''
# body
# div[4]
# table 
# tr[1]
# td[1]
# div[0]
# table[0] id....
# '''

# # CONSOLIDATED STATEMENT OF OPERATIONS:                             table id="idm139639486070472"
# # CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME:                   table id="idm139639486972888"
# # CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME (Parenthetical):   table id="idm139639487227816"
# # CONSOLIDATED BALANCE SHEET:                                       table id="idm139639491907368"
# # CONSOLIDATED BALANCE SHEET (Parenthetical):                       table id="idm139639491869128"
# # CONSOLIDATED STATEMENT OF CASH FLOWS:                             table id="idm139639492530216"
# # CONSOLIDATED STATEMENT OF EQUITY:                                 table id="idm139639704543944"
# # CONSOLIDATED STATEMENT OF EQUITY (Parenthetical):                 table id="idm139639485795432"





# # # for row in doc_table[0].find_all('tr')[0:32]:
# # for row in doc_table[0]:
# #     tr=row.find_all('tr')[0:32]

# #     if len(tr) !=0:
# #         for row in tr:





# #             # find all the columns
# #             cols = row.find_all('td')

# #                 # if there are no columns move on to the next row.
# #             if len(cols) != 0:        
                
# #                 # grab headers:
# #                 title =
# #                 frequency =
# #                 date1 =
# #                 date2 =
# #                 date3 =



# #                 # grab the text
# #                 NET_REVENUE = cols[0].find('a', {'href':True})#, 'id':'interactiveDataBtn'})
# #                 net_revenue = cols[1].text.strip()
# #                 net_revenue = cols[3].text.strip()
# #                 COST_AND_EXPENCES = cols[1].find('a', {'href':True})#, 'id':'interactiveDataBtn'})
# #                 cost_of_revenue = cols[3].text.strip()

# #                 # find the links
# #                 filing_doc_href = cols[2].find('a', {'href':True})       #, 'id':'documentsbutton'})
# #                 # filing_int_href = cols[1].find('a', {'href':True, 'id':'interactiveDataBtn'})
# #                 filing_num_href = cols[2].find('a')

# #                 for row in doc_table[0].find_all('tr')[1:2]:
# #                     cols = row.find_all('td')
# #                     if len(cols) != 0:
# #                         filing_type = cols[1].text.strip()
# # ____________________________________________________________________________________________________________









































# # TRY NR. 2 
# # Grab the whole table from Interactive data "View Filing Data": 
# link="https://www.sec.gov/cgi-bin/viewer?action=view&cik=1090872&accession_number=0001090872-21-000027&xbrl_type=v"
# # ____________________________________________________________________________________________________________



# third_link='https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&accession_number=0000320193-21-000105&xbrl_type=v'


# # doclinks examples: 
# a_2020='/Archives/edgar/data/1090872/000109087220000020/R1.htm'
# a_2021='/Archives/edgar/data/1090872/000109087221000027/R1.htm'
aapl_2021='https://www.sec.gov/Archives/edgar/data/320193/000032019321000105/R1.htm'
aapl_2021='https://www.sec.gov/Archives/edgar/data/320193/000032019321000105/R1.htm'
aapl_2021='https://www.sec.gov/Archives/edgar/data/1090872/000032019321000105.htm'
# cik = 1090872 #get from cik-dataframe
cik = 320193 #get from cik-dataframe
doc_numb = 'R1'
parsed = urlparse(third_link)
query = parse_qs(parsed.query)
[accession_number] = query['accession_number']
accession_number=re.sub('\D', '', accession_number)


baselink= 'https://www.sec.gov'
link_builder=baselink+"/Archives/edgar/data/"+str(cik)+"/"+str(accession_number)+"/"+doc_numb+".htm"
print("")
print("LINK TO TABLE: "+link_builder)


req = requests.get(link_builder,headers=hdr)
print(req.status_code)
soup = BeautifulSoup(req.text, 'html.parser')
print(soup.prettify)
doc_table = soup.find_all('table')#, class_ ='tableFile')

master_list = []

    # print(cols)

for row in doc_table[0].find_all('tr'):
    
    # find all the columns
    cols = row.find_all('td')#, class_='pl')

        # if there are no columns move on to the next row.
    if len(cols) != 0:        
        
        # grab the text
        filing_text1 = cols[0].text.strip()
        filing_text2 = cols[1].text.strip()
        filing_text3 = cols[2].text.strip()
        filing_numb = cols[3].text.strip()
  
        # # find the links
        # filing_doc_href = cols[2].find('a', {'href':True})       #, 'id':'documentsbutton'})
        # # filing_int_href = cols[1].find('a', {'href':True, 'id':'interactiveDataBtn'})
        # filing_num_href = cols[2].find('a')

        # for row in doc_table[0].find_all('tr')[1:2]:
        #     cols = row.find_all('td')
        #     if len(cols) != 0:
        #         filing_type = cols[1].text.strip()

# create and store data in the dictionary
        file_dict = {}
        file_dict['filing_text1'] = filing_text1
        file_dict['filing_text2'] = filing_text2
        file_dict['filing_text3'] = filing_text3
        file_dict['filing_numb'] = filing_numb
    
        # # let the user know it's working
        print('-'*100)        
        print("filing_text1: " + filing_text1)
        print("filing_text2: " + filing_text2)
        print("filing_text3: " + filing_text3)
        print("filing_numb: " + filing_numb)
        


    # filing_text = cols[0].text.strip()
    # filing_numb2 = cols[2].text.strip()

    # print("filing_text"+row+": "+filing_text)
    # print("filing_numb"+row+": "+filing_text)

# tr class="re"
# <td class="pl" 
# td class="nump">


#     <tr class="ro">
# 0   <td class="pl" style="border-bottom: 0px;" valign="top"><a class="a" href="javascript:void(0);" onclick="top.Show.showAR( this, 'defref_dei_EntityPublicFloat', window );">Entity Public Float</a></td>
# 1  <td class="text"> <span></span>
#     </td>
# 2    <td class="text"> <span></span>
#     </td>
# 3    <td class="nump">$ 2,021,360<span></span>
#     </td>
#     </tr>



# ''
# #FOR REFERENCE: 
# stat_equity = soup.find_all('table', id ='idm139639704543944')

# doc_table = soup.find_all('table', class_='tableFile2')

# base_url_sec = r"https://www.sec.gov"

# for row in doc_table[0].find_all('tr')[0:3]:
    
#     # find all the columns
#     cols = row.find_all('td')

# '''







# # # ____________________________________________________________________________________________________________






































































# # TRY NR. 3   
# # Interact with "download as lxml file" from Interactive data: 
# # ____________________________________________________________________________________________________________
# # link="https://www.sec.gov/cgi-bin/viewer?action=view&cik=1090872&accession_number=0001090872-21-000027&xbrl_type=v"







# # ____________________________________________________________________________________________________________














# '''
# CUTOUT OF HTML; ONLY FOR REFERANCE
# _____________________________________________________________________________________________________________________________________________________________________________________________________________________
# From ROUND 2's site 

# #                 <tr>
# #             0       <td scope="row">1</td>
# #             1       <td scope="row">10-K</td>
# #             2       <td scope="row"><a href="/ix?doc=/Archives/edgar/data/1090872/000109087221000027/a-20211031.htm">a-20211031.htm</a>   <span style="color: green">iXBRL</span></td>
# #             3       <td scope="row">10-K</td>
# #             4       <td scope="row">4539259</td>
# #                 </tr>

# From ROUND 1's site 
#                     # <tr>
#                     # <td nowrap="nowrap">10-K</td>
#                     # <td nowrap="nowrap"><a href="/Archives/edgar/data/1090872/000109087221000027/0001090872-21-000027-index.htm" id="documentsbutton"> Documents</a>  <a href="/cgi-bin/viewer?action=view&amp;cik=1090872&amp;accession_number=0001090872-21-000027&amp;xbrl_type=v" id="interactiveDataBtn"> Interactive Data</a></td>
#                     # <td class="small">Annual report [Section 13 and 15(d), not S-K Item 405]<br/>Acc-no: 0001090872-21-000027 (34 Act)  Size: 22 MB             </td>
#                     # <td>2021-12-17</td>
#                     # <td nowrap="nowrap"><a href="/cgi-bin/browse-edgar?action=getcompany&amp;filenum=001-15405&amp;owner=exclude&amp;count=100">001-15405</a><br/>211502413         </td>
#                     # </tr>
# _____________________________________________________________________________________________________________________________________________________________________________________________________________________
# '''






















# #################################################################################################################################################################
# #                                          ROUND 4: Downlaod Document: From All found elements --> Save as .CSV
# #################################################################################################################################################################


# '''
# TO-DO: 
# ____________________________

# (1) import & edit code from scraper_options_yf.py




# ____________________________

# '''
