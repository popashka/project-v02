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

cnt = 0

q = deque()
qm = deque()
qq = deque()


while True:
    url = r'https://spbexchange.ru/ru/market-data/default.aspx'

    tables = pd.read_html(url)

    international_companies = tables[0]

    df2 = pd.DataFrame(data=international_companies)

    alibaba = df2.loc[df2['Идентиф. Код ЦБ', 'Идентиф. Код ЦБ'] == 'YNDX']

    price = float(alibaba.iat[0, 3]) / 100
    if (price < 10):
        price = price * 10

    q.append(price)
    qq.append(datetime.datetime.now())

    print(price)

    url = r'https://www.londonstockexchange.com/market-stock/0EDM/yandex-nv/overview'

    response = requests.get(url)
    print(response.status_code)


    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)

    all = soup.findAll('span', class_='price-tag')
    ldn_baba = all[0].text

    url = r'https://ru.investing.com/equities/yandex?cid=102063'

    response = requests.get(url)
    print(response.status_code)


    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)

    all = soup.findAll('span', class_='text-2xl')
    msc_baba = all[0].text
    qm.append(msc_baba)

    url4 = 'https://ru.investing.com/currencies/usd-rub'
    response = requests.get(url4)
    print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    all1 = soup.findAll('span', class_='text-2xl')

    if (cnt >= 3):
        d = {'SPB R': [q.popleft()], 'LDN, $': [ldn_baba], 'MSC R' : [qm.popleft()], 'time' : qq.popleft(),
             '$~R': all1[0].text}
        df = pd.DataFrame(data=d)
        df.to_csv('yndx.csv', mode='a', index=False, header=False)

    cnt = cnt + 1
    time.sleep(0)