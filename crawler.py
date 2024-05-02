import requests
from bs4 import BeautifulSoup
from lxml import etree,html
import pandas as pd
from datetime import date
import time

crypt_data = []
for i in range(1, 2):
    url = f"https://crypto.com/price?page={i}"
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')
    dom = etree.HTML(str(soup))
    cryptic = soup.find_all('tr', attrs={"class": "css-1cxc880"})
    for crypt in cryptic:
        name = crypt.find("p", attrs={"class": "chakra-text css-rkws3"}).text
        abbr = crypt.find("span", attrs={"class": "chakra-text css-1jj7b1a"}).text
        crypturl = "https://crypto.com"+crypt.find("a", attrs={"class": "chakra-link css-tzmkfm"})['href']
        price = crypt.find("p", attrs={"class": "chakra-text css-13hqrwd"}).text.replace("$", "").replace(",", "")
        #change24hrs = dom.xpath(f'//*[@id="__next"]/div[3]/div[2]/div/div[3]/div[3]/table/tbody/tr[{i}]/td[5]/p')[0].text
        req2 = requests.get(crypturl).text
        soup2 = BeautifulSoup(req2, 'lxml')
        dom2 = html.fromstring(req2)
        marketcap = soup2.find('p', attrs={'class': 'chakra-text css-1c8c51m'}).text.replace("$", "").replace(",", "").replace(" B", "")
        volume24hrs = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[2]/p/text()')
        circulatingsupply = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[3]/p/text()')
        maxsupply = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[4]/p/text()')
        totalsupply = dom2.xpath('//*[@id="__next"]/div[3]/div/div/div[3]/div[1]/div[1]/div[3]/div[5]/p/text()')
        crypto = {
            "name": name,
            "abbr": abbr,
            "crypturl": crypturl,
            "price": price,
            "volume24hrs": volume24hrs,
            "marketcap": marketcap,
            "circulatingsupply": circulatingsupply,
            "maxsupply": maxsupply
        }
        crypt_data.append(crypto)
    print(f"Data {i} recorded")
    break

dataset = pd.DataFrame(crypt_data)
dataset.to_csv("Crypto.csv", index=False)

