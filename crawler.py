import requests
from bs4 import BeautifulSoup
from lxml import etree, html
import pandas as pd
import random
from datetime import datetime, timedelta
import warnings


def refine_data(dataset):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dataset = pd.DataFrame(dataset)
        dataset['volume24hrs'] = dataset['volume24hrs'].astype(str).str.replace('[','').str.replace("'", "").str.replace('$', '').str.replace(' M','').str.replace(']', '').str.replace('B','').str.strip()
        dataset['marketcap'] = dataset['marketcap'].astype(str).str.replace('[','').str.replace("'", "").str.replace('$', '').str.replace(' M','').str.replace(']', '').str.replace('B','').str.strip()
        dataset['circulatingsupply'] = dataset['circulatingsupply'].astype(str).str.replace('[','').str.replace("'", "").str.replace('$', '').str.replace(' M','').str.replace(']', '').str.replace('B','').str.replace(r'[^\d.]', '', regex=True)
        dataset['maxsupply'] = dataset['maxsupply'].astype(str).str.replace('[','').str.replace("'", "").str.replace('$', '').str.replace(' M','').str.replace(']', '').str.replace('B','').str.replace(r'[^\d.]', '', regex=True)
        dataset['totalsupply'] = dataset['totalsupply'].astype(str).str.replace('[','').str.replace("'", "").str.replace('$', '').str.replace(' M','').str.replace(']', '').str.replace('B','').str.replace(r'[^\d.]', '', regex=True)
        return dataset


def generate_data():
    crypt_data = []
    for i in range(1, 428):
        url = f"https://crypto.com/price?page={i}"
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'lxml')
        #dom = etree.HTML(str(soup))
        cryptic = soup.find_all('tr', attrs={"class": "css-1cxc880"})
        for crypt in cryptic:
            name = crypt.find("p", attrs={"class": "chakra-text css-rkws3"}).text
            abbr = crypt.find("span", attrs={"class": "chakra-text css-1jj7b1a"}).text
            crypturl = "https://crypto.com"+crypt.find("a", attrs={"class": "chakra-link css-tzmkfm"})['href']
            price = crypt.find("p", attrs={"class": "chakra-text css-13hqrwd"}).text.replace("$", "").replace(",", "")
            #change24hrs = dom.xpath(f'//*[@id="__next"]/div[3]/div[2]/div/div[3]/div[3]/table/tbody/tr[{i}]/td[5]/p')[0].text
            req2 = requests.get(crypturl).text
            #soup2 = BeautifulSoup(req2, 'lxml')
            dom2 = html.fromstring(req2)
            marketcap = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[1]/p/text()')
            volume24hrs = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[2]/p/text()')
            circulatingsupply = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[3]/p/text()')
            maxsupply = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[4]/p/text()')
            totalsupply = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[5]/p/text()')
            start_date = datetime(2020, 1, 1)
            end_date = datetime.now()
            delta = end_date - start_date
            random_days = random.randint(0, delta.days)
            date_taken = start_date + timedelta(days=random_days)
            crypto = {
                "name": name,
                "abbr": abbr,
                "crypturl": crypturl,
                "price": price,
                "volume24hrs": volume24hrs,
                "marketcap": marketcap,
                "circulatingsupply": circulatingsupply,
                "maxsupply": maxsupply,
                "totalsupply": totalsupply,
                "date_taken": date_taken
            }
            crypt_data.append(crypto)
            cleaned_data = refine_data(crypt_data)
        print(f"Data {i} recorded")

    dataset = pd.DataFrame(cleaned_data)
    dataset.to_csv("Crypto.csv", index=False)
    dataset.to_json("Crypto.json", orient="records")


generate_data()
