import pandas as pd
import numpy as np
import yfinance as yf
import concurrent.futures
import time
from functools import cache

start=time.perf_counter()

@cache
def do_something(secs):
  a = yf.Ticker(secs).info.get('ebitda', 'NaN')
  b = yf.Ticker(secs).info.get('enterpriseValue', 'NaN')
  EvEbitda=b/a
  print(f'{secs}´s EV/EBITDA: {EvEbitda}')
  return 


@cache
def main():
  with concurrent.futures.ThreadPoolExecutor() as executer:
    secs = ['AAPL', 'GOOGL', 'FB']
    results = executer.map(do_something, secs)
    for result in results:
      print(result)

main()


finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s)')
