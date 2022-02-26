import pandas as pd
import numpy as np
import yfinance as yf

tickers = ['AAPL', 'GOOGL', 'FB']

for t in tickers:
  a = yf.Ticker(t).info.get('ebitda', 'NaN')
  b = yf.Ticker(t).info.get('enterpriseValue', 'NaN')
  # c = yf.Ticker(t).info.get('totalAssets', 'NaN')
  EvEbitda=b/a
  print(t,"EV/EBITDA: ",EvEbitda)

