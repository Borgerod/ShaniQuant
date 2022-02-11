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


link = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1090872&type=10-k&dateb=dt&owner=exclude&start=&output=&count=100'


# def get_data(link):
hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}

req = requests.get(link,headers=hdr)
req.raise_for_status()
print(req.status_code)
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
    
        # let the user know it's working
        # print('-'*100)        
        # print("Filing Type: " + filing_type)
        # print("Filing Date: " + filing_date)
        # print("Filing Number: " + filing_numb)
        # print("Document Link: " + filing_doc_link)
        # print("Filing Number Link: " + filing_num_link)
        # print("Interactive Data Link: " + filing_int_link)
        
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
for report in master_list[0:2]:
    
    print('-'*100)
    # print(report['links']['documents'])
    # print(report['links']['filing_number'])
    # print(report['links']['interactive_data'])
    
# MIN EDIT___________________________________________________________________________________
# Filen jeg vil ha:   0001090872-21-000027.txt

second_link=filing_doc_link
# second_link='https://www.sec.gov/Archives/edgar/data/1090872/000109087221000027/0001090872-21-000027-index.htm'
req = requests.get(second_link,headers=hdr)
# print(req.status_code)
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
        filing_numb = cols[2].text.strip()
        
        # find the links
        filing_doc_href = cols[2].find('a', {'href':True})       #, 'id':'documentsbutton'})
        # filing_int_href = cols[1].find('a', {'href':True, 'id':'interactiveDataBtn'})
        filing_num_href = cols[2].find('a')

        for row in doc_table[0].find_all('tr')[1:2]:
            cols = row.find_all('td')
            if len(cols) != 0:
                filing_type = cols[1].text.strip()



# # FRA DENNE SIDEN

#                 <tr>
#             0       <td scope="row">1</td>
#             1       <td scope="row">10-K</td>
#             2       <td scope="row"><a href="/ix?doc=/Archives/edgar/data/1090872/000109087221000027/a-20211031.htm">a-20211031.htm</a>   <span style="color: green">iXBRL</span></td>
#             3       <td scope="row">10-K</td>
#             4       <td scope="row">4539259</td>
#                 </tr>

# # FRA FORJE SIDE
                    # <tr>
                    # <td nowrap="nowrap">10-K</td>
                    # <td nowrap="nowrap"><a href="/Archives/edgar/data/1090872/000109087221000027/0001090872-21-000027-index.htm" id="documentsbutton"> Documents</a>  <a href="/cgi-bin/viewer?action=view&amp;cik=1090872&amp;accession_number=0001090872-21-000027&amp;xbrl_type=v" id="interactiveDataBtn"> Interactive Data</a></td>
                    # <td class="small">Annual report [Section 13 and 15(d), not S-K Item 405]<br/>Acc-no: 0001090872-21-000027 (34 Act)  Size: 22 MB             </td>
                    # <td>2021-12-17</td>
                    # <td nowrap="nowrap"><a href="/cgi-bin/browse-edgar?action=getcompany&amp;filenum=001-15405&amp;owner=exclude&amp;count=100">001-15405</a><br/>211502413         </td>
                    # </tr>






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
    
        # let the user know it's working
        # print('-'*100)        
        # print("Filing Type: " + filing_type)
        # print("Filing Date: " + filing_date)
        # print("Filing Number: " + filing_numb)
        # print("Document Link: " + filing_doc_link)
        # print("Filing Number Link: " + filing_num_link)
        # print("Interactive Data Link: " + filing_int_link)
        
        # append dictionary to master list
        master_list.append(file_dict)

# RUNDE 2_______________________________________________________________________________________________



second_link=filing_doc_link
req = requests.get(second_link,headers=hdr)
soup = BeautifulSoup(req.content, 'html.parser')
# print(soup.prettify)
stat_operations = soup.find_all('table', id ='idm139639486070472')
# stat_income = soup.find_all('table', id ='idm139639486972888')
# balance_sheet = soup.find_all('table', id ='idm139639491907368')
# stat_cashflow = soup.find_all('table', id ='idm139639492530216')
# stat_equity = soup.find_all('table', id ='idm139639704543944')
master_list = []

'''
body
div[4]
table 
tr[1]
td[1]
div[0]
table[0] id....
'''

# CONSOLIDATED STATEMENT OF OPERATIONS:                             table id="idm139639486070472"
# CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME:                   table id="idm139639486972888"
# CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME (Parenthetical):   table id="idm139639487227816"
# CONSOLIDATED BALANCE SHEET:                                       table id="idm139639491907368"
# CONSOLIDATED BALANCE SHEET (Parenthetical):                       table id="idm139639491869128"
# CONSOLIDATED STATEMENT OF CASH FLOWS:                             table id="idm139639492530216"
# CONSOLIDATED STATEMENT OF EQUITY:                                 table id="idm139639704543944"
# CONSOLIDATED STATEMENT OF EQUITY (Parenthetical):                 table id="idm139639485795432"




# for row in doc_table[0].find_all('tr')[0:32]:
for row in doc_table[0]:
    tr=row.find_all('tr')[0:32]:

    if len(tr) !=0:
        for row in tr:





    # find all the columns
    cols = row.find_all('td')

        # if there are no columns move on to the next row.
    if len(cols) != 0:        
        
        # grab headers:
        title =
        frequency =
        date1 =
        date2 =
        date3 =



        # grab the text
        NET_REVENUE = cols[0].find('a', {'href':True})#, 'id':'interactiveDataBtn'})
        net_revenue = cols[1].text.strip()
        net_revenue = cols[3].text.strip()
        COST_AND_EXPENCES = cols[1].find('a', {'href':True})#, 'id':'interactiveDataBtn'})
        cost_of_revenue = cols[3].text.strip()

        # find the links
        filing_doc_href = cols[2].find('a', {'href':True})       #, 'id':'documentsbutton'})
        # filing_int_href = cols[1].find('a', {'href':True, 'id':'interactiveDataBtn'})
        filing_num_href = cols[2].find('a')

        for row in doc_table[0].find_all('tr')[1:2]:
            cols = row.find_all('td')
            if len(cols) != 0:
                filing_type = cols[1].text.strip()

# # FRA DENNE SIDEN

#                 <tr>
#             0       <td scope="row">1</td>
#             1       <td scope="row">10-K</td>
#             2       <td scope="row"><a href="/ix?doc=/Archives/edgar/data/1090872/000109087221000027/a-20211031.htm">a-20211031.htm</a>   <span style="color: green">iXBRL</span></td>
#             3       <td scope="row">10-K</td>
#             4       <td scope="row">4539259</td>
#                 </tr>

# # FRA FORJE SIDE
                    # <tr>
                    # <td nowrap="nowrap">10-K</td>
                    # <td nowrap="nowrap"><a href="/Archives/edgar/data/1090872/000109087221000027/0001090872-21-000027-index.htm" id="documentsbutton"> Documents</a>  <a href="/cgi-bin/viewer?action=view&amp;cik=1090872&amp;accession_number=0001090872-21-000027&amp;xbrl_type=v" id="interactiveDataBtn"> Interactive Data</a></td>
                    # <td class="small">Annual report [Section 13 and 15(d), not S-K Item 405]<br/>Acc-no: 0001090872-21-000027 (34 Act)  Size: 22 MB             </td>
                    # <td>2021-12-17</td>
                    # <td nowrap="nowrap"><a href="/cgi-bin/browse-edgar?action=getcompany&amp;filenum=001-15405&amp;owner=exclude&amp;count=100">001-15405</a><br/>211502413         </td>
                    # </tr>


# __________________________________________________________________________________________



# # ***
# # ## Section Four: Parsing the XML version
# # We saw up above that if we set the `output` parameter to `atom,` that we get back an XML version of the same data, so let's explore how to request and parse the XML output. When we are defining the output parameter, we are accessing the RSS Feed that is linked with EDGAR. While the above example does work relatively easily, it probably makes more sense to use the RSS Feed as the data returned to us is more structured and therefore easier to parse.

# # The request will be identical except for the fact that we will change the `output` parameter to `atom` and change the parser to `lxml`.

# # # In[7]:


# # # base URL for the SEC EDGAR browser
# # endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

# # # define our parameters dictionary
# # param_dict = {'action':'getcompany',
# #               'CIK':'1265107',
# #               'type':'10-k',
# #               'dateb':'20190101',
# #               'owner':'exclude',
# #               'start':'',
# #               'output':'atom',
# #               'count':'100'}

# # # request the url, and then parse the response.
# # response = requests.get(url = endpoint, params = param_dict)
# # soup = BeautifulSoup(response.content, 'lxml')

# # # Let the user know it was successful.
# # print(response.stat)
# # print('Request Successful')
# # print(response.url)



# link = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1090872&dateb=20190101&owner=exclude&start=&output=atom&count=100'


# # def get_data(link):
# hdr = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36'}

# req = requests.get(link,headers=hdr)
# req.raise_for_status()
# print(req.status_code)
# content = req.content
# # return content
# # data = get_data(test_URL)

# soup = BeautifulSoup(req.content, 'lxml')

# # print(soup.prettify)




# # ***
# # Once we have the content, we need to a search for all the `entry` tags as these tags contain the info related to the filings. 
# # Each entry tag has the following structure:

# # data="""
# # # <entry>
# # #     <category label="form type" scheme="https://www.sec.gov/" term="10-K"></category>
# # #     <content type="text/xml">
# # #         <accession-nunber></accession-nunber>
# # #         <act></act>
# # #         <file-number></file-number>
# # #         <file-number-href></file-number-href>
# # #         <filing-date></filing-date>
# # #         <filing-href></filing-href>
# # #         <filing-type></filing-type>
# # #         <film-number></film-number>
# # #         <form-name></form-name>
# # #         <size></size>
# # #         <xbrl_href></xbrl_href>
# # #     </content>
# # #     <id></id>
# # #     <link href="" rel="alternate" type="text/html"/>
# # #     <summary type="html"></summary>
# # #     <title></title>
# # #     <updated></updated>
# # # </entry>
# # """

# # Please keep in mind that I have removed the actual info for readability.

# # In[56]:




# # find all the entry tags
# entries = soup.find_all('entry')
# # # initalize our list for storage
# master_list_xml = []

# # loop through each found entry, remember this is only the first two
# for entry in entries[0:3]:
    
#     # grab the accession number so we can create a key value
#     accession_num=soup.find("accession-number").text

#     # create a new dictionary
#     entry_dict = {}
#     entry_dict[accession_num] = {}
    
#     # store the category info
#     category_info = entry.find('category')    
#     entry_dict[accession_num]['category'] = {}
#     entry_dict[accession_num]['category']['label'] = category_info['label']
#     entry_dict[accession_num]['category']['scheme'] = category_info['scheme']
#     entry_dict[accession_num]['category']['term'] =  category_info['term']

#     # store the file info
#     entry_dict[accession_num]['file_info'] = {}
#     entry_dict[accession_num]['file_info']['act'] = entry.find('act').text
#     entry_dict[accession_num]['file_info']['file_number'] = entry.find('file-number').text
#     entry_dict[accession_num]['file_info']['file_number_href'] = entry.find('file-number-href').text
#     entry_dict[accession_num]['file_info']['filing_date'] =  entry.find('filing-date').text
#     entry_dict[accession_num]['file_info']['filing_href'] = entry.find('filing-href').text
#     entry_dict[accession_num]['file_info']['filing_type'] =  entry.find('filing-type').text
#     entry_dict[accession_num]['file_info']['form_number'] =  entry.find('film-number').text
#     entry_dict[accession_num]['file_info']['form_name'] =  entry.find('form-name').text
#     entry_dict[accession_num]['file_info']['file_size'] =  entry.find('size').text
    
#     # store extra info
#     entry_dict[accession_num]['request_info'] = {}
#     entry_dict[accession_num]['request_info']['link'] =  entry.find('link')['href']
#     entry_dict[accession_num]['request_info']['title'] =  entry.find('title').text
#     entry_dict[accession_num]['request_info']['last_updated'] =  entry.find('updated').text
    
#     # store in the master list
#     master_list_xml.append(entry_dict)
    
#     print('-'*100)
#     print(entry.find('form-name').text)
#     print(entry.find('file-number').text)
#     print(entry.find('file-number-href').text)
#     print(entry.find('link')['href'])


# # ***
# # Now that we have all the entries stored in our dictionary let's grab the first item and see what the output looks like for the category section.

# # In[50]:


# import pprint
# # pprint.pprint(master_list_xml[0]['0001265107-18-000013']['category'])
# pprint.pprint(master_list_xml)


# # ***
# # ## Parsing the Next Page
# # In the example above our results were limited because we did such a narrow search, but it's not uncommon for more broad searches to return over 100 different entries. In these situations, we can leverage the XML output to find the link that takes us to the additional results. This process is easy; we merely find the `link` tag that has a `rel` attribute set to `next`. To demonstrate this, I've added a new URL that will return over 100 results.

# # In[55]:


# # base URL for the SEC EDGAR browser
# endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

# # define our parameters dictionary
# param_dict = {'action':'getcompany',
#               'CIK':'1265107',
#               'dateb':'20190101',
#               'owner':'exclude',
#               'start':'',
#               'output':'atom',
#               'count':'100'}

# # request the url, and then parse the response.
# response = requests.get(url = endpoint, params = param_dict)
# soup = BeautifulSoup(response.content, 'lxml')

# # find the link that will take us to the next page
# links = soup.find_all('link',{'rel':'next'})

# # while there is still a next page
# while soup.find_all('link',{'rel':'next'}) != []:

#     # grab the link
#     next_page_link = links[0]['href']  
    
#     print('-'*100)
#     print(next_page_link)
    
#     # request the next page
#     response = requests.get(url = next_page_link)
#     soup = BeautifulSoup(response.content, 'lxml')
    
#     # see if there is a next link
#     links = soup.find_all('link',{'rel':'next'})


# # ***
# # ## Closing Remarks
# # The EDGAR query system allows us to quickly filter the companies we want to grab filings for and makes the process of finding the forms we need intuitive. With our knowledge of Python and the request system that EDGAR uses we can gain access to a tremendous amount of financial data that is free for public use.


