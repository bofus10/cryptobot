#
#Library to handle coingecko api
#

import requests
import json

class Gecko():

  #def __init__(self):
    #not really necessary


  def tick(self,symbol):
    url = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd".format(symbol)
    #head = Bittrex._pre(self,url,"GET")
    
    #response = json.loads((requests.request("GET", url, headers=Bittrex.headers)).text)
    print((requests.request("GET", url)).text)
    
    
  def find_coin(self,call):
    url = "https://api.coingecko.com/api/v3/coins/list"
    #head = Bittrex._pre(self,url,"GET")
    
    #response = json.loads((requests.request("GET", url, headers=Bittrex.headers)).text)
    coin_list = json.loads((requests.request("GET", url)).text)
    #if symbol not in coin_list:
    #  print("no coin found")
    #else:  
    for coin in coin_list:
      if coin["symbol"] == call or coin["name"] == call or coin["id"] == call:
        print("Found: {}".format(coin))


#r1 = Gecko()
#r1.tick("ethereum,bitcoin")
#r1.find_coin("ripple")