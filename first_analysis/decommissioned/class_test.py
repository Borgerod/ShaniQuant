import pandas as pd

class storage:
    '''
    Storage class, purpose:
        Instead of having a list of variables that gets passed through all of the functions without them needing to, they could instead be saved in this storage class. 
        Now, the functions will only recieve only the variables that they need and only return new variables.
        If a function needs a variable that is not from the function right over it (but futher up in the script) it can simply get it by calling the class. 
    '''
    def __init__(self, symbol, ind, ev_ebitda, eval_ALL, eval_tot, eval_tot_ALL, eval_SPY, diff, diff_ALL, diff_tot, diff_tot_ALL, diff_SPY, fin_score, ev_ebitda_ind, ev_ebitda_ind_ALL, ev_ebitda_total,ev_ebitda_total_ALL, ev_ebitda_SPY):
        self.symbol              = symbol
        self.ind                 = ind
        self.ev_ebitda           = ev_ebitda
        self.eval_ALL            = eval_ALL
        self.eval_tot            = eval_tot
        self.eval_tot_ALL        = eval_tot_ALL
        self.eval_SPY            = eval_SPY
        self.diff                = diff
        self.diff_ALL            = diff_ALL
        self.diff_tot            = diff_tot
        self.diff_tot_ALL        = diff_tot_ALL
        self.diff_SPY            = diff_SPY
        self.fin_score           = fin_score
        self.ev_ebitda_ind       = ev_ebitda_ind
        self.ev_ebitda_ind_ALL   = ev_ebitda_ind_ALL
        self.ev_ebitda_total     = ev_ebitda_total
        self.ev_ebitda_total_ALL = ev_ebitda_total_ALL
        self.ev_ebitda_SPY       = ev_ebitda_SPY
        # return ind, ev_ebitda


print("-"*50)
print("")

# def symbol():
#     symbol=['AAPL', 'TSLA', 'MSFT']
#     return symbol

# def make_list(i):
#     fin_score=['100','200','300']
#     # for i in fin_score:
#     # s=storage("",fin_score,"","","","","","","","","","","","","","","","")
#     # print(f"Current fin_score in Storage: {s.fin_score}")
#     return fin_score

# def main():
#     symbol_list=symbol()
#     for i in symbol_list:
#         fin_score=make_list(i)
#         i=storage(i,"","","","","","","","","","","","","","","","","")
#         i=storage("",fin_score,"","","","","","","","","","","","","","","","")
#         print(f'Storage of {fin_score} complete')
#         print(f"Current symbol in Storage: {i.symbol}")
#         print(f"Current fin_score in Storage: {i.fin_score}")
#         print("-"*50)
#         print("")

# main()
# def traficker():
#     master_list=[]
#     symbol_list=symbol()
#     for i in symbol_list:
#         lst=make_list(i)
#         master_list.append(lst)
#     return master_list, symbol_list




def symbol():
    symbol=['AAPL', 'TSLA', 'MSFT']
    return symbol

def read_info(i):
    file_path=(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_yf\data_scraping_info\\'+i+'_info.csv')
    return pd.read_csv(file_path, names=["subject", "info"]).drop([0]).reset_index(drop=True)

def get_industry(i):
    info=read_info(i)
    info.set_index(['subject'], inplace=True)
    ind=info.loc['industry'][0]
    ev_ebitda=info.loc['enterpriseToEbitda'][0]
    i=storage("",ind,ev_ebitda,"","","","","","","","","","","","","","","")
    # print(f"Current ind in Storage: {store.ind}")
    return i, ind, ev_ebitda





def main():
    symbol_list=symbol()
    for i in symbol_list:
        s =get_industry(i)
        # print(i)
        # print(ind)
        # print(ev_ebitda)
        i=storage(i,"","","","","","","","","","","","","","","","","")
        




        print(f"Current symbol in Storage: {i.symbol}")
        print(f"Current ind in Storage: {s.ind}")
        print(f"Current ev_ebitda in Storage: {s.ev_ebitda}")
        print("-"*50)
        print("")
main()

