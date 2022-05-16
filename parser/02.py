from IPython.display import display
import pandas as pd
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from collections import deque
import datetime
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

q = deque()
qq = deque()
qm = deque()
cnt = 0

while True:
    url = r'https://spbexchange.ru/ru/market-data/default.aspx'

    tables = pd.read_html(url)

    international_companies = tables[0]

    df2 = pd.DataFrame(data=international_companies)

    tcs = df2.loc[df2['Идентиф. Код ЦБ', 'Идентиф. Код ЦБ'] == 'TCS']

    print(tcs.iat[0, 3])
    price = float(tcs.iat[0, 3]) / 100.0
    print(price)
    if price < 10:
        price = price * 10

    q.append(price)
    qq.append(datetime.datetime.now())

    url = r'https://www.londonstockexchange.com/stock/TCS/tcs-group-holding-plc/company-page'

    response = requests.get(url)
    print(response.status_code)


    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)

    all = soup.findAll('span', class_='price-tag')
    ldn_tcs = all[0].text

    url = r'https://ru.investing.com/equities/tcs-group-holding-plc?cid=1153662'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    all = soup.findAll('span', class_='text-2xl')
    msc_tcs = all[0].text
    qm.append(msc_tcs)

    url4 = 'https://ru.investing.com/currencies/usd-rub'
    response = requests.get(url4)
    print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    all1 = soup.findAll('span', class_='text-2xl')
    print(all1[0].text)

    if (cnt >= 3) :
        d = {'SPB R': [q.popleft()], 'LDN, $': [ldn_tcs], 'MSC R' : [qm.popleft()], 'time' : qq.popleft(),
             '$~R': all1[0].text}
        df = pd.DataFrame(data=d)
        df.to_csv('tcs2.csv', mode='a', index=False, header=False)

    cnt = cnt + 1
    time.sleep(300)

