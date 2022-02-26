import pandas as pd

#_____________OPTIONS______________
# pd.options.display.max_rows=None
# pd.options.display.max_columns=5
# pd.options.display.width=20000
#__________________________________


'''
_____________________________NOTE / CLARIFICATION______________________________

This code was meant as a ONE-TIME-USE code and has for now served it's purpose.

If you're wondering where the files: 
"backup_organisert_yahoo_split.xlsx" & "backup_organisert_ind.xlsx" comes from, 
they don't come from any code, they were manually organized by me using excel. 
_______________________________________________________________________________

''' 

def get_yahoo_org():
    file_path = (r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\organisert_yahoo.xlsx')
    yahoo_org = pd.read_excel(file_path)
    yahoo_org = pd.DataFrame(yahoo_org)
    yahoo_org = yahoo_org.set_index(yahoo_org.iloc[:,0])
    yahoo_org = yahoo_org.iloc[:,1:2]
    return yahoo_org

def get_ind_org():
    # file_path = (r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\backup_organisert_ind.xlsx'))
    file_path = (r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\organisert_ind.xlsx')
    ind_org = pd.read_excel(file_path)
    ind_org = pd.DataFrame(ind_org)
    ind_org = ind_org.set_index(ind_org.iloc[:,0])
    ind_org = ind_org.iloc[:,1:2]
    return ind_org

def renamer_n_concat():
    yahoo_org = get_yahoo_org().rename(columns = {'Yahoo_finance_Industry_list': 'Industry Name'})
    df = pd.concat([get_ind_org(), yahoo_org], axis = 0, ignore_index = False)
    return df

def new_dataframe():
    df = renamer_n_concat()
    new_df = (df.assign(labels = df.groupby(level = 0).cumcount())
                .groupby([df.index,'labels']).first()
                .unstack('labels')
                .sort_index(axis = 1 , level = 1)
                .droplevel(1 , axis = 1))
    return new_df

def new_columns():
    new_df=new_dataframe()
    new_df.columns = [''] * len(new_df.columns)
    new_df.columns = [
        'Industry Name1',
        'Industry Name2',
        'Industry Name3',
        'Industry Name4',
        'Industry Name5',
        'Industry Name6',
        'Industry Name7',
        'Industry Name8',
        'Industry Name9',
        'Industry Name10',
        ]
    return new_df

def column_compiler():
    new_df = new_columns()
    new_df["Industry Name"] = new_df["Industry Name1"].astype(str)+","+new_df["Industry Name2"].astype(str)+","+new_df["Industry Name3"].astype(str)+","+new_df["Industry Name4"].astype(str)+","+new_df["Industry Name5"].astype(str)+","+new_df["Industry Name6"].astype(str)+","+new_df["Industry Name7"].astype(str)+","+new_df["Industry Name8"].astype(str)
    new_df['Industry Name'] = new_df['Industry Name'].str.replace(',nan',"")
    new_df['Industry Name'] = new_df['Industry Name'].str.replace(',None',"")
    new_df['Industry Name'] = new_df['Industry Name'].str.replace(','," , ")
    newer_df = new_df['Industry Name']
    return newer_df

def newer_df_saver():
    return column_compiler().to_excel(r'C:\Users\Big Daddy B\Documents\GitHub\Quant-algo-Part-1-_-The-Screener\project\data_storage\data_scraping_ticker_list\Updated_Industry_Names.xlsx', index=True)
newer_df_saver()
