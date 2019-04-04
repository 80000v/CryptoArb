#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-27 21:40:03
# @Author  : KlausQiu
# @Link    : https://www.kraken.com/
# @Version : $$$1.0$$$

import sys
sys.path.append("../../../strategy")

import kraken_util as ku
import httplib
import json
import urlparse
import time
from collections import defaultdict
import requests
from decimal import Decimal


def chooseType(coinType):
    # usdt_btc EOSUSD
    pay = coinType.split("_")[0]
    coin = coinType.split("_")[1]
    if pay == "usdt":
        pay = "usd"
    return coin.upper() + pay.upper()

class kraken:
    def __init__(self, account=""):
        self.account = account

    def get_tickers(self,coinType,method="ticker"):
        coinType = chooseType(coinType)
        url = urlparse.urlparse(ku.API_HOST).hostname
        try:
            conn = httplib.HTTPSConnection(url,timeout=2)
            conn.request('GET','/0/public/Ticker?pair=%s'%coinType)
            ticker = json.loads(conn.getresponse().read())
            import pdb; pdb.set_trace()
            _result = ticker["result"][coinType]

            _result = {"buyOne":_result["b"][0],"sellOne":_result["a"][0]}
            return _result
        except BaseException as e:
            return {"result":"fail","msg":"%s"%e}


    def getAccountInfo(self,method="get_account_info"):
        try:
            method = "Balance"
            result = ku.query_private(method,account=self.account)
            coins = ["eos","usd","neo"]
            result = result["result"]
            _result = {}
            for c in result:
                _result[c[1:]] = result[c]
            for c in coins:
                if c not in result.keys():
                    _result[c] = {"available": 0, "frozen": 0}
            return result
        except BaseException as e:
            return {"result":"fail","msg":"%s"%e}

    def buy(self, coinType, price, amount, method="AddOrder"):
        coinType = chooseType(coinType)
        params = {'pair': coinType,
                  'price': price,
                  'volume': amount,
                  'type': "buy",
                  'ordertype': "limit"}
        result = ""
        try:
            result = ku.query_private(method, params, account=self.account)
            return result
        except BaseException as e:
            return {"result": "fail", "msg": "%s_%s" %(e,result)}

    def sell(self, coinType, price, amount, method="AddOrder"):
        coinType = chooseType(coinType)
        params = {'pair': coinType,
                  'price': price,
                  'volume': amount,
                  'type': "sell",
                  'ordertype': "limit"}
        result = ""
        try:
            result = ku.query_private(method, params, account=self.account)
            return result
        except BaseException as e:
            return {"result": "fail", "msg": "%s_%s" % (e, result)}

    def cancelOrder(self, coinType, id, method="cancel_order"):
        coinType = chooseType(coinType)
        params = {"txid":id}
        result = ""
        try:
            result = ku.query_private(method, params, account=self.account)
            return result
        except BaseException as e:
            return {"result": "fail", "msg": "%s_%s" % (e, result)}

    def getOrderInfo(self, coinType, id, method="order_info"):
        coinType = chooseType(coinType)
        params = {"txid": id}
        result = ""
        try:
            result = ku.query_private(method, params, account=self.account)
            return result
        except BaseException as e:
            return {"result": "fail", "msg": "%s_%s" % (e, result)}
    
    def order(self,pair,price,volume,Type,ordertype,method="AddOrder"):
        '''
        params = {'pair': 'XXBTZEUR',
            'type': 'buy',
            'ordertype': 'limit',
            'price': '1',
            'volume': '1',
            'close[pair]': 'XXBTZEUR',
            'close[type]': 'sell',
            'close[ordertype]': 'limit',
            'close[price]': '9001',
            'close[volume]': '1'}
        '''
        method = 'AddOrder'
        params = {'pair': pair,
            'price': price,
            'volume': volume,
            'type': Type,
            'ordertype': ordertype}
        result = ku.query_private(method, params, account=self.account)
        return result

    def getOrders(self, coinType, method="OpenOrders"):
        coinType = chooseType(coinType)
        method = 'OpenOrders'
        params = {"pair": coinType}
        result = ""
        try:
            result = ku.query_private(method, params, account=self.account)
            return result
        except BaseException as e:
            return {"result": "fail", "msg": "%s_%s" % (e, result)}

    def QueryOrders(self,method=""):
        method = 'QueryOrders'
        params = {"txid":'1111'}
        result = ku.query_private(method, params, account=self.account)
        return result 

if __name__ == '__main__':
    k = kraken(account="huangxinyu")
    # print k.get_tickers("usd_eos")
    # print k.getAccountInfo()
    print k.buy("usd_xrp", 1, 30)
