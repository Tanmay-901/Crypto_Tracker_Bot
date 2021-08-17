import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

coinlist = ['bitcoin', 'Dogecoin', 'Nano']
coinlist = "%2C".join(coinlist)
pricelist = []

fetch = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coinlist}&vs_currencies=inr").json()
price_data = list(fetch.items())
for coin, price in price_data:
    print(coin, ": ₹", fetch[coin]['inr'] * 1.115)
# print(fetch)
