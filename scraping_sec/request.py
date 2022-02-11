start = 2019
end = 2020
cik = 220000320193
short_cik = str(cik)[-6:] #we will need it later to form urls

import requests
from bs4 import BeautifulSoup as bs 
url = f"https://www.sec.gov/cgi-bin/srch-edgar?text=cik%3D%{cik}%22+AND+form-type%3D(10-q*+OR+10-k*)&first={start}&last={end}"
# url='https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1265107&dateb=20190101&owner=exclude&start=&output=atom&count=100'

req = requests.get(url)
print(req.url)
soup = bs(req.text,'lxml')


acc_nums = []
for link in soup.select('td>a[href]'):
    target = link['href'].split(short_cik,1)    
    if len(target)>1:
        acc_num = target[1].split('/')[1]
        if not acc_num in acc_nums: #we need this filter because each filing has two forms: text and html, with the same accession number
            acc_nums.append(acc_num)
            print(acc_nums)
            print(acc_num)


# fs_url = f"https://www.sec.gov/Archives/edgar/data/{short_cik}/{acc_nums[2]}/Financial_Report.xlsx"
# fs = requests.get(fs_url)
# with open('random_edgar.xlsx', 'wb') as output:
#     output.write(fs.content)