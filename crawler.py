import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd


crypt_data = []
for i in range(1, 10):
    url = f"https://crypto.com/price?page={i}"
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')
    dom = etree.HTML(str(soup))
    cryptic = soup.find_all('tr',attrs={"class":"css-1cxc880"})
    for crypt in cryptic:
        name = crypt.find("p", attrs={"class": "chakra-text css-rkws3"}).text
        abbr = crypt.find("span", attrs={"class": "chakra-text css-1jj7b1a"}).text
        price = crypt.find("p", attrs={"class": "chakra-text css-13hqrwd"}).text.replace("$", "").replace(",", "")
        change24hrs = dom.xpath(f'//*[@id="__next"]/div[3]/div[2]/div/div[3]/div[3]/table/tbody/tr[{i}]/td[5]/p')[0].text
        volume24hrs = dom.xpath(f'//*[@id="__next"]/div[3]/div[2]/div/div[3]/div[3]/table/tbody/tr[{i}]/td[6]')[0].text.replace("$", "").replace(",", "").replace(" B", "")
        marketcap = dom.xpath(f'//*[@id="__next"]/div[3]/div[2]/div/div[3]/div[3]/table/tbody/tr[{i}]/td[7]')[0].text.replace("$", "").replace(",", "").replace(" B", "")
        crypto = {
            "name": name,
            "abbr": abbr,
            "price": price,
            "change24hrs": change24hrs,
            "volume24hrs": volume24hrs,
            "marketcap": marketcap
        }
        crypt_data.append(crypto)
    print(f"Data {i} recorded")

dataset = pd.DataFrame(crypt_data)
dataset.to_csv("Crypto.csv", index=False)
