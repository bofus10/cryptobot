#
# Library to handle telegram api
#

import gecko as gc
import bittrex_calls as bt

import configparser
import requests
import json


class Telegram():

    def __init__(self):
        self._offset = 0
        self._query = []
        self._chatid = ""
        parse = configparser.ConfigParser()
        parse.read("config/properties")
        if parse.get("bot", "chat_id") and parse.get("bot", "bot_id"):
            #self._chatid = parse.get("bot", "chat_id")
            self._botid = parse.get("bot", "bot_id")
        else:
            print("No Bot Set, please verify your config file")
            exit(1)

    def getUpdates(self):

        url = "https://api.telegram.org/bot{}/getUpdates?offset={}".format(self._botid, self._offset)

        resp = json.loads((requests.request("GET", url)).text)

        if resp["ok"]:
            if len(resp["result"]) > 0:
                for msg in resp["result"]:
                    toadd = {
                        "user_id": msg["message"]["from"]["id"],
                        "username": msg["message"]["from"]["username"],
                        "chat_id": msg["message"]["chat"]["id"],
                        "text": msg["message"]["text"],
                        "Iscommand": True if "entities" in msg["message"] else False,
                    }
                    self._chatid = msg["message"]["chat"]["id"]
                    self._offset = msg["update_id"]
                    self._query.append(toadd)

                    # print("{};{};{};{};{}".format(self._offset,user_id,username,chat_id,text))

                    # Was the last message? then we clean
                    if msg == resp["result"][-1]:
                        # print("this is the end")
                        url = "https://api.telegram.org/bot{}/getUpdates?offset={}".format(self._botid, self._offset + 1)
                        requests.request("GET", url)

                return True
            else:
                # print("no message")
                return False


    def pushMSG(self,msg):
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(self._botid,self._chatid,msg)
        requests.request("GET", url)

    def prepareResponse(self):
        for msg in self._query:
            print(msg)
            if msg["Iscommand"]:
                received = str(msg["text"]).replace('/', '').split()
                print("{};{}".format(received[0],received[1]))

                if received[0] == "coin":
                    resp = json.loads(gc.Gecko.tick(received[1].upper()))
                    print(resp[received[1]]["usd"])
                    Telegram.pushMSG(self,"$"+str(resp[received[1]]["usd"]))
                #if received[0] == "track":
                    #implement Start, Stop, status of which current coins are tracked help and save info
                    #start polling data whena  coin is start track
                #if received[0] == "threshold":
                    # implement set, clear, help and save info
                elif received[0] == "bittrex-balance":
                    if len(received) > 1:
                        bt.Bittrex.balance(self,received[1].upper())
                    else:
                        bt.Bittrex.balance(self)
                elif received[0] == "bittrex-bid-ask":
                    bt.Bittrex.markets(self, received[1].upper())
                #if received[0] == "set":
                    # implement bittrex secret,key to file
                else:
                    print("!!Error")


b1 = Telegram()

if b1.getUpdates():
    b1.prepareResponse()
else:
    print("No message")

# get with default
# student.get('subject', 'Science')
