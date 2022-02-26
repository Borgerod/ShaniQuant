import concurrent.futures
import time
import yfinance as yf


start=time.perf_counter()


X=(r'/')

PATH=(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_yf\\')

def actions(func,s):
   symbol=yf.Ticker(s)
   category="actions"
   file_name=s+"_"+category+".csv"
   print(".."+category)
   return 

def do_something_else(sec):
   print(f'actions() is downloading {sec}...')

   symbol=yf.Ticker(sec)
   df=symbol.actions
   category="actions"
   print(".."+category)
   file_name=sec+"_"+category+".csv"
   df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
   return sec

def do_something(sec): 
   print(f'calender() is downloading {sec}...')
   symbol=yf.Ticker(sec)
   df=symbol.actions
   category="calendar"
   print(".."+category)
   file_name=sec+"_"+category+".csv"
   df.to_csv(PATH+"data_scraping_"+category+X+file_name, index=True, header=True)
   return sec

def main():
   with concurrent.futures.ThreadPoolExecutor() as executer:
      sec=['msft','aapl','tsla']
      fn_list=[do_something, do_something_else]
      # enum_fn=enumerate(fn_list)
      # for i, func, sec, in zip(enum_fn,fn_list,sec):
      # for i, sec in enumerate(sec):
      # for func , sec in zip(sec, fn_list):
      for i, func in enumerate(fn_list):
      # for func in (fn_list):
         print(fn_list)
         print(sec[i])



         # print(func)
         # print(sec[i])
         # print(fn_list)
      # for i in fn_list:
         # print(i)
      # print("_"*80)

      # results = executer.map(i, sec)
      results = executer.map(sec[i], func)
      print(results)
      # for result in results:
        # print(result)



      # for sec in sec:
      #    print(sec)
      #    for i in fn_list:
      #       print(i)
      #    print("_"*80)

      #    results = executer.map(i, sec)

      # for result in results:
      #    print(result)




      # for i, func in enumerate(fn_list):
      #    print(i)
      #    print(func)
      #    print(sec)
      #    results = executer.map(func, sec)

      # for result in results:
      #    print(result)



if __name__ == '__main__':
   main()

# import cProfile
# import pstats
# with cProfile.Profile() as pr:
#    do_something_else(sec)
# stats=pstats.Stats(pr)
# stats.sort_stats(pstats.SortKey.TIME)
# stats.print_stats()
# stats.dump_stats(filename='needs_profiling.prof')
finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s)')
