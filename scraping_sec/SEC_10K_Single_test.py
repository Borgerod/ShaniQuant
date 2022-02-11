import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1', # Do Not Track Request Header 
    'Connection'      : 'close'
    }


# define the base url needed to create the file url.
base_url = r"https://www.sec.gov/Archives/edgar/data/"

cik_num='/886982/'
url= base_url+cik_num+"/index.json"
# # convert a normal url to a document url
# normal_url = r"https://www.sec.gov/Archives/edgar/data/1265107/0001265107-19-000004.txt"
# normal_url = normal_url.replace('-','').replace('.txt','/index.json')

# # define a url that leads to a 10k document landing page
# documents_url = r"https://www.sec.gov/Archives/edgar/data/1265107/000126510719000004/index.json"

# request the url and decode it.
req=requests.get(url, headers=headers).json()
decoded_content=content.json()


# for file in content['directory']['item']:
    
#     # Grab the filing summary and create a new url leading to the file so we can download it.
#     if file['name'] == 'FilingSummary.xml':

#         xml_summary = base_url + content['directory']['name'] + "/" + file['name']
        
#         print('-' * 100)
#         print('File Name: ' + file['name'])
#         print('File Path: ' + xml_summary)       

