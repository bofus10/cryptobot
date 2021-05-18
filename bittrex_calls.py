#
# Library to handle bittrex api
#
import configparser

import requests
import time
import hmac
import hashlib
import base64
import json


class Bittrex():

    #def __init__(self, secret, apikey):
    #    self._secret = secret
    #    self._api_key = apikey

    def _pre(self, url, method, body=""):
        #we need to verify secret and key are set
        parse = configparser.ConfigParser()
        parse.read("config/properties")

        if parse.get("bittrex","secret") and parse.get("bittrex","key"):
            self._secret = str(parse.get("bittrex", "secret"))
            self._api_key = parse.get("bittrex", "key")

            headers = {}
            self._body = body
            self._method = method
            # digest = hmac.new(secret_key, msg=thing_to_hash, digestmod=hashlib.sha512).digest()

            secret = self._secret
            headers["Content-Type"] = "application/json"
            headers["api-key"] = self._api_key
            headers["api-timestamp"] = str(int(round(time.time() * 1000)))
            headers["api-content-hash"] = hashlib.sha512(str(self._body).encode("utf-8")).hexdigest()
            s = "{}{}{}{}".format(headers["api-timestamp"], url, self._method, headers["api-content-hash"])
            headers["api-signature"] = hmac.new(secret.encode(), msg=s.encode(), digestmod=hashlib.sha512).hexdigest()
            # print(headers["api-signature"])

            return headers
        else:
            print("Error Bittrex Credentials not set")

    # returns balances of the account
    def balance(self, symbol=""):
        url = "https://api.bittrex.com/v3/balances/{}".format(symbol)
        print(url)
        head = Bittrex._pre(self, url, "GET")

        # response = json.loads((requests.request("GET", url, headers=Bittrex.headers)).text)
        print((requests.request("GET", url, headers=head)).text)
        # print("{}\n{}\n".format(response["symbol"],response["name"]))

    # Returns wallet Address, or opens a new one
    def address(self, method, symbol=""):

        if method == "GET":
            url = "https://api.bittrex.com/v3/addresses/{}".format(symbol)
            head = Bittrex._pre(self, url, method)

            # response = json.loads((requests.request("GET", url, headers=Bittrex.headers)).text)
            print((requests.request(method, url, headers=head)).text)
            # print("{}\n{}\n".format(response["symbol"],response["name"]))
            # {"code":"NOT_FOUND"} No address, do a POST
            # {"status":"PROVISIONED","currencySymbol":"ETC","cryptoAddress":"0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}

        elif method == "POST":  # add err in case of INVALID_PERMISSION
            url = "https://api.bittrex.com/v3/addresses"
            if symbol == "":
                print("trhow exception")

            query = {
                "currencySymbol": symbol
            }
            payload = json.dumps(query)
            head = Bittrex._pre(self, url, method, payload)
            print((requests.request(method, url, data=payload, headers=head)).text)
            # RESPONSE: {"status":"REQUESTED","currencySymbol":"ETC"}

    # Returns state of currency
    def currency(self, symbol=""):
        url = "https://api.bittrex.com/v3/currencies/{}".format(symbol)
        head = Bittrex._pre(self, url, "GET")

        # response = json.loads((requests.request("GET", url, headers=Bittrex.headers)).text)
        print((requests.request("GET", url, headers=head)).text)
        # print("{}\n{}\n".format(response["symbol"],response["name"]))
        # {"symbol":"ETH","name":"Ethereum","coinType":"ETH","status":"ONLINE","minConfirmations":36,"notice":"","txFee":"0.00730000","logoUrl":"https://bittrexblobstorage.blob.core.windows.net/public/7e5638ef-8ca0-404d-b61e-9d41c2e20dd9.png","prohibitedIn":[],"baseAddress":"0xfbb1b73c4f0bda4f67dca266ce6ef42f520fbb98","associatedTermsOfService":[],"tags":[]}

    # Returns bid/ask of market, example: ETH-USD or ETH-BTC
    def markets(self, symbol):
        url = "https://api.bittrex.com/v3/markets/{}-USD/ticker".format(symbol)
        head = Bittrex._pre(self, url, "GET")

        # response = json.loads((requests.request("GET", url, headers=Bittrex.headers)).text)
        print((requests.request("GET", url, headers=head)).text)
        # print("{}\n{}\n".format(response["symbol"],response["name"]))

    def orders(self, method, state, symbol=""):

        if method == "GET":
            url = "https://api.bittrex.com/v3/orders{}".format(state)
            head = Bittrex._pre(self, url, method)

            # response = json.loads((requests.request("GET", url, headers=Bittrex.headers)).text)
            print((requests.request(method, url, headers=head)).text)
            # print("{}\n{}\n".format(response["symbol"],response["name"]))
            # {"code":"NOT_FOUND"} No address, do a POST
            # {"status":"PROVISIONED","currencySymbol":"ETC","cryptoAddress":"0xXXXXXX"}

        elif method == "POST":  # add err in case of INVALID_PERMISSION
            url = "https://api.bittrex.com/v3/orders"
            if symbol == "":
                print("trhow exception")

            query = {
                "marketSymbol": "string",
                "direction": "string",  # BUY, SELL
                "type": "string",  # LIMIT, MARKET, CEILING_LIMIT, CEILING_MARKET
                "quantity": "number (double)",
                # quantity (optional, must be included for non-ceiling orders and excluded for ceiling orders)
                "ceiling": "number (double)",
                # optional, must be included for ceiling orders and excluded for non-ceiling orders
                "limit": "number (double)",
                # optional, must be included for LIMIT orders and excluded for MARKET orders)
                "timeInForce": "string",
                # GOOD_TIL_CANCELLED, IMMEDIATE_OR_CANCEL, FILL_OR_KILL, POST_ONLY_GOOD_TIL_CANCELLED, BUY_NOW, INSTANT
                "clientOrderId": "string (uuid)",  # Optional for advance order tracking
                "useAwards": "boolean"  # Optional to use Bittrex Credits
            }
            payload = json.dumps(query)
            head = Bittrex._pre(self, url, method, payload)
            print((requests.request(method, url, data=payload, headers=head)).text)
            # RESPONSE: {"status":"REQUESTED","currencySymbol":"ETC"}

#r1 = Bittrex()
#r1.balance("ETH")
# r1.address("GET","VET")
# r1.currency("ETH")
#r1.markets("ETH")
