#
#Library to handle telegram api
#

import requests
import json


class Telegram():

  def __init__(self):
    self._offset = 0

  def getUpdates(self,botID):
  
    url = "https://api.telegram.org/bot{}/getUpdates?offset={}".format(botID,self._offset)
    
    resp = json.loads((requests.request("GET", url)).text)
    
    if resp["ok"] == True:
      for msg in resp["result"]:
        self._offset = msg["update_id"]
        user_id = msg["message"]["from"]["id"]
        username = msg["message"]["from"]["username"]
        chat_id = msg["message"]["chat"]["id"]
        text = msg["message"]["text"]
        
        print("{};{};{};{};{}".format(self._offset,user_id,username,chat_id,text))
        
        #Is command?
        if "entities" in resp["result"]:
          print("Is a command")
          
  


#b1 = Telegram()
#b1.getUpdates("BOT_TOKEN")