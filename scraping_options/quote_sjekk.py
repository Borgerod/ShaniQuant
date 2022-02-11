import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

df = pd.read_csv (r'~\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\Prosjekt\data_storage\data_scraping_options\data_quotes.csv')
print(df)