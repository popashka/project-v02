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
cnt = 0

while True:
    url = r'https://spbexchange.ru/ru/market-data/default.aspx'
    tables = pd.read_html(url)
    international_companies = tables[0]
    russian_companies = tables[1]

    df = pd.DataFrame(data=russian_companies)
    df2 = pd.DataFrame(data=international_companies)

    lukoil = df.loc[df['Идентиф. Код ЦБ', 'Идентиф. Код ЦБ'] == 'LKOH']

    #print(lukoil)

    price = lukoil.iat[0,3]

    print(price)
    q.append(price)
    qq.append(datetime.datetime.now())

    url = 'https://tools.morningstar.co.uk/uk/stockreport/default.aspx?SecurityToken=0P0000DGH3]3]0]E0WWE$$ALL'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    all = soup.findAll('span', class_='price')
    lukoil_ldn = all[0].text
    print(lukoil_ldn)

    url3 = 'https://www.finam.ru/quote/moex-akcii/lukoil/'
    response = requests.get(url3)
    print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    all = soup.findAll('span', class_='PriceInformation__price--26G')
    print(all[0].text)

    url4 = 'https://ru.investing.com/currencies/usd-rub'
    response = requests.get(url4)
    print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    all1 = soup.findAll('span', class_='text-2xl')
    print(all1[0].text)


    if (cnt >= 3) :
        d = {'SPB R': [q.popleft()], 'LDN, $': [lukoil_ldn], 'MSC R' : [all[0].text], 'time' : qq.popleft(),
             '$~R': all1[0].text}
        df = pd.DataFrame(data=d)
        df.to_csv('luk.csv', mode='a', index=False, header=False)

    cnt = cnt + 1
    time.sleep(300)

# gazprom
# tcs
# Globaltrans
# x5retailgroup
# 