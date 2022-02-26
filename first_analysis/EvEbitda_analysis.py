import pandas as pd
import datetime as dt
from industry_intel import *
import time

start = time.perf_counter()


#_____________OPTIONS______________
pd.options.display.max_columns=None
# pd.options.display.max_rows=None
# # pd.options.display.width=None
pd.set_option('display.width', 3000)
#__________________________________


#_____________NOTES______________
# EV/EBITDA by Sector: /Industryhttps://siblisresearch.com/data/ev-ebitda-multiple/
# get_ev_ebitda_SPY() er IKKE ferdig, trenger å finne en kilde å gjøre et request fra. 
#__________________________________


def get_ev_ebitda_SPY():
    ev_ebitda_SPY = 14.20 # [PLACEHOLDER] [PLACEHOLDER] [PLACEHOLDER]
    return ev_ebitda_SPY

def symbol():
    file_path = (r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\tickerlist_nyse_nasdaq.csv')
    symbol = pd.read_csv(file_path, names=['Symbol','Name'])
    # return symbol
   
    # symbol =['AAPL', 'TSLA', 'MSFT']  # [PLACEHOLDER] [PLACEHOLDER] [PLACEHOLDER]
    # return symbol                     # [PLACEHOLDER] [PLACEHOLDER] [PLACEHOLDER]
    

def read_info(i):
    file_path = (r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_yf\data_scraping_info\\'+i+'_info.csv')
    return pd.read_csv(file_path, names = ["subject", "info"]).drop([0]).reset_index(drop = True)

def get_industry(i):
    info = read_info(i)
    info.set_index(['subject'], inplace=True)
    ind = info.loc['industry'][0]
    ev_ebitda = info.loc['enterpriseToEbitda'][0]
    return ind, ev_ebitda

def match_industry(i):
    lst=[]
    df = ev_ebitda_byIndustry()
    ind, ev_ebitda = get_industry(i)
    filter1 = df[df['Industry_Name'].str.contains(f"(?i){ind}")]
    a, b, c, d = float(filter1['EV/EBITDA']), float(filter1['EV/EBITDA_ALL']),float(df['EV/EBITDA'][95:96]), float(df['EV/EBITDA_ALL'][95:96])
    m_list=[float(ev_ebitda), a, b, c, d]
    lst.extend(m_list)
    return lst

def check_diff(i):
    lst = match_industry(i)
    lst.append(get_ev_ebitda_SPY())
    [a,b,c,d,e,f]=lst
    diff=[]
    for i in lst[1:]:
        x = ((a-i)/a*100)
        diff.append(x)
    lst.extend(diff)
    return lst

def analyse_diff(i):
    lst = check_diff(i)
    diff=lst[6:]
    eval_list=[]
    for d in diff:
        # v='eval_'+n
        if d<=-25:   
            val=1
        elif 10>=d<=-10:
            val=2
        elif -10<=d<=10:
            val=3   
        elif 25>=d>=10:
            val=4
        elif d>=25:
            val=5
        eval_list.append(val)
    lst.extend(eval_list)
    return lst

def final_score(i):
    lst = analyse_diff(i)
    # f_lst=lst[-5:]
    lst.extend([round(sum(lst[-5:])/5)])
    return lst

def final_score_phrase(i):
    lst = final_score(i) 
    f=lst[-1:][0]
    if f==1:
        lst.append('Very Undervalued')
    elif f==2:
        lst.append('Undervalued')
    elif f==3:
        lst.append('Normally Valued')
    elif f==4:
        lst.append('Overvalued')
    elif f==5:
        lst.append('Very Overvalued')
    return lst        

def traficker():
    master_list=[]
    symbol_list=symbol()
    for i in symbol_list:
        lst=final_score_phrase(i)
        master_list.append(lst)
    return master_list, symbol_list

def evaluation_dataframe():
    master_list, symbol_list=traficker()
    # df_list=[]
    for i in symbol_list:
        EVEBIDTA_eval_df=pd.DataFrame(master_list,
                            columns=[
                            'EV/Ebitda', 
                            'EV/Ebitda ind', 'diff %',  
                            'EV/Ebitda ind ALL', 'diff ALL %',  
                            'EV/Ebitda total', 'diff tot %',
                            'EV/Ebitda total ALL','diff tot ALL %',
                            'EV/Ebitda SPY', 'diff SPY %',
                            'Score: Industry', 'Score: ALL Industries',
                            'Score: Total Market', 'Score: Total Market ALL', 
                            'Score: S&P 500', 'Final Score', 'Evaluation'
                                    ], index=symbol_list)
    print(EVEBIDTA_eval_df)
    return EVEBIDTA_eval_df 
evaluation_dataframe()

# def eval_saver():
#     return evaluation_dataframe().to_excel(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_first_analysis\EVEBIDTA_eval_df.xlsx', index=True, header=True)

finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s)')
