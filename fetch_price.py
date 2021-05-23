import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
coinlist = ['bitcoin', 'Dogecoin']
pricelist = []
for coin in coinlist:
  fetch = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=inr").json()
  fetch = str(list(fetch.keys())[0]) + ": " + ("%.2f" % (float(list(fetch.values())[0]['inr']) * 1.115)) + "\n"
  # print(fetch)
  pricelist.append(fetch)
print(pricelist)
