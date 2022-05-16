import datetime

from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

url = 'https://www.boerse-frankfurt.de/en/etf/21shares-ethereum-etp'
url2 = 'https://www.boerse-stuttgart.de/de-de/produkte/etps/etns/stuttgart/a2t68z-21-shares-ethereum-etp-aeth'
url3 = 'https://www.bxswiss.com/instruments/CH0454664027'
url4 = 'https://www.six-group.com/en/products-services/the-swiss-stock-exchange/market-data/etp/etp-explorer/etp-detail.CH0454664027EUR4.html'
url5 = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=CHF&To=EUR'

option = webdriver.ChromeOptions()
option.add_argument("--headless")
wasbid = 0
wasask = 0
wb1 = 0
wa1 = 0
wb2 = 0
wa2 = 0
wb3 = 0
wa3 = 0
wasrank = 0

while(1 < 2):
    driver = webdriver.Chrome(executable_path='/home/popashka/chromedriver', options=option)

    driver.get(url5)

    html = driver.page_source

    driver.close()

    soup = BeautifulSoup(html, 'html.parser')

    data = soup.findAll('p', class_='result__BigRate-sc-1bsijpp-1 iGrAod')
    try:
        str = data[0].text
        str1, str2 = str.split('E')
        frank = float(str1)
    except:
        frank = wasfrank

    wasfrank = frank
    print(frank)

    if frank == 0:
        frank = 0.98


    driver = webdriver.Chrome(executable_path='/home/popashka/chromedriver', options=option)

    driver.get(url)

    html = driver.page_source

    driver.close()

    soup = BeautifulSoup(html, 'html.parser')

    data = soup.findAll('td', class_='widget-table-cell askBidLimit')

    print("Bid is:")
    try:
        print(data[0])
        bidx = float(data[0].text)
    except:
        bidx = wasbid

    data = soup.findAll('td', class_='widget-table-cell askBidLimit text-right')

    print("Ask is:")
    try:
        print(data[0].text)
        kek = float(data[0].text.strip())
    except:
        kek = wasask

    askx = kek
    wasask = askx
    wasbid = bidx

    pricex = (bidx + askx) / 2


    driver = webdriver.Chrome(executable_path='/home/popashka/chromedriver', options=option)

    driver.get(url2)

    html = driver.page_source

    driver.close()

    soup = BeautifulSoup(html, 'html.parser')

    data = soup.findAll('span', id='js-bsg-fs-assessment-bid-field')

    try:
        print("Bid is:")
        print(data[0].text)
        str = data[0].text
        str = str.replace(',', '.')
        bid = float(str)
    except:
        bid = wb1

    wb1 = bid
    bid *= frank


    data = soup.findAll('span', id='js-bsg-fs-assessment-ask-field')

    print("Ask is:")
    try:
        print(data[0].text)
        str = data[0].text
        str = str.replace(',', '.')
        ask = float(str)
    except:
        ask = wa1

    wa1 = ask
    ask *= frank

    price = (bid + ask) / 2

    driver = webdriver.Chrome(executable_path='/home/popashka/chromedriver', options=option)

    driver.get(url3)

    html = driver.page_source

    driver.close()

    soup = BeautifulSoup(html, 'html5lib')

    data = soup.findAll('dd', class_='heading heading--large heading--compact animate-tick js-bid')

    print("Bid is:")
    try:
        print(data[0].text)
        bidbx = float(data[0].text)
    except:
        bidbx = wb2

    wb2 = bidbx
    data = soup.findAll('dd', class_='heading heading--large heading--compact animate-tick js-ask')

    print("Ask is:")
    try:
        print(data[0].text)
        askbx = float(data[0].text)
    except:
        askbx = wa2

    wa2 = askbx
    pricebx = (askbx + bidbx) / 2
    print("kek")

    driver = webdriver.Chrome(executable_path='/home/popashka/chromedriver', options=option)

    driver.get(url4)

    time.sleep(5)

    html = driver.page_source

    driver.close()

    soup = BeautifulSoup(html, 'html.parser')

    data = soup.findAll('dd', class_='data-pair-value')

    print("Bid is:")
    try:
        print(data[1].text)
        str = data[1].text
        bidd, askd = str.split('/')
        bids = float(bidd)
        asks = float(askd)
    except:
        bids = wb3
        asks = wa3

    wb3 = bids
    wa3 = asks

    print(bids)
    print(asks)
    prices = (bids + asks) / 2

    d = {'Xetra Bid': [bidx], 'Xetra Ask': [askx], 'Xetra Price': [pricex],
         'Stut Bid': [bid], 'Stut Ask': [ask], 'Stut Price': [price],
         'BX Bid': [bidbx], 'BX Ask': [askbx], 'BX Price': [pricebx],
         'Six Bid': [bids], 'Six Ask': [asks], 'Six Price': [prices],
         'time': [datetime.datetime.now()]}
    df = pd.DataFrame(data=d)
    df.to_csv('pars-eth.csv', mode='a', index=False, header=False)

    time.sleep(58)



# Volume 500
# Price in euros