import yfinance as yf
import concurrent.futures
import time
from functools import cache
import datetime as dt

start=time.perf_counter()

class Context:   
    def __init__(self):  
        self.current_dt=datetime.datetime.now()


# @cache
# def get_ebidta_ev(secs):
#   a = yf.Ticker(secs).info.get('ebitda', 'NaN')
#   b = yf.Ticker(secs).info.get('enterpriseValue', 'NaN')
#   EvEbitda=b/a
#   print(f'{secs}´s EV/EBITDA: {EvEbitda}')
#   return secs

@cache
def get_ebidta_ev(secs):
  a = yf.Ticker(secs).info.get('ebitda', 'NaN')
  b = yf.Ticker(secs).info.get('enterpriseValue', 'NaN')
  EvEbitda=b/a
  print(f'{secs}´s EV/EBITDA: {EvEbitda}')
  return secs, EvEbitda


@cache
def evebidta_executer():
  with concurrent.futures.ThreadPoolExecutor() as executer:
    secs = ['AAPL', 'GOOGL', 'FB']
    results = executer.map(get_ebidta_ev, secs)
    EvEbidta_list=[]
    for result in results:
      EvEbidta_list.append(result)
      # print(result)
      # return result
  print(EvEbidta_list)
  return EvEbidta_list
evebidta_executer()
# if __name__ == '__main__':
#   main()

finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s)')
