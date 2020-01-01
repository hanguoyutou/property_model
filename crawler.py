import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
from processing import data_process

def generate_urls():
    example_url = 'https://www.property.hk/eng/tran.php?bldg=&prop=R&size=&year=2012&month=2&select=&page=1&dt=&tab=TRAN'

    year = []
    for y in range(8):      #change back to 8 after testing
        year.append(2012+y)

    month = []
    for m in range(12):
        month.append(1+m)

    page = []
    for p in range(20):
        page.append(1+p)

    urls = []
    url_a = 'https://www.property.hk/eng/tran.php?bldg=&prop=R&size=&year='
    url_b = '&month='
    url_c = '&select=&page='
    url_d = '&dt=&tab=TRAN'
    for y in year:
        for m in month:
            for p in page:
                url = url_a+str(y)+url_b+str(m)+url_c+str(p)+url_d
                urls.append(url)
    return urls

def crawling(url):
    '''
    get the raw_data
    '''
    s = requests.Session()
    response = s.get(
        url=url,
        allow_redirects=False
    )
    html = response.text
    soup = BeautifulSoup(html,'lxml')
    data = []
    for i in soup.select('div#proplist .border tr td.hidden-xs'):
        data.append(i.get_text())
    sdata = np.asarray(data)
    sdata = sdata.reshape((20,9))
    # print(sdata.T)
    href = []
    for i in soup.select('div#proplist .border tr td.hidden-xs a'):
        href.append('property.hk'+str(i.attrs['href']))
    shref = np.asarray(href)
    shref = np.array(shref.reshape((20,2))[:,0])
    # print(shref)
    combined = np.append(sdata.T,shref).reshape((10,20)).T
    return combined[combined[:,4] != '']

if __name__ == '__main__':
    urls = generate_urls()
    filename = 'dataset.csv'
    column_names = ['Time','Year','Month','Location','District','Building','Floor','Unit','Area(ft^2)','Price(M)','Price/ft^2','Reference']

    for url in urls:
        raw_data = crawling(url)
        data = data_process(raw_data=raw_data)
        df = pd.DataFrame(data,columns=column_names)
        if not os.path.isfile(filename):
            df.to_csv(filename,index=False)
        else:
            df.to_csv(filename, mode='a', header=False,index=False)