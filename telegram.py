#
#Library to handle telegram api
#

import requests
import json


class Telegram():

  def __init__(self):
    self._offset = 0
    self._query = {};

  def getUpdates(self,botID):
  
    url = "https://api.telegram.org/bot{}/getUpdates?offset={}".format(botID,self._offset)
    
    resp = json.loads((requests.request("GET", url)).text)

    if resp["ok"] == True:
      if len(resp["result"]) > 0:
        for msg in resp["result"]:
          self._offset = msg["update_id"]
          self._query["user_id"] = msg["message"]["from"]["id"]
          self._query["username"] = msg["message"]["from"]["username"]
          self._query["chat_id"] = msg["message"]["chat"]["id"]
          self._query["text"] = msg["message"]["text"]
          
          #print("{};{};{};{};{}".format(self._offset,user_id,username,chat_id,text))

          #Is command?
          if "entities" in msg["message"]:
            self._query["Iscommand"] = True
          else:
            self._query["Iscommand"] = False
            
          print(self._query)  
            
          #Was the last message? then we clean  
          if msg == resp["result"][-1]:
            print("this is the end")
            url = "https://api.telegram.org/bot{}/getUpdates?offset={}".format(botID,self._offset+1)
            requests.request("GET", url)
            
      else:
        print("no message")
        
  #define simlpe mesage push
  #def pushMSG(self,msg):
  
  
  #def prepareResponse(self)
  


b1 = Telegram()
b1.getUpdates("")

# get with default
#student.get('subject', 'Science')