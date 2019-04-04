#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-28 17:40:03
# @Author  : KlausQiu
# @Link    : https://www.binance.com
# @Version : $$$1.0$$$
import sys
sys.path.append("../../../strategy")
from binanceClient import Client
from util.util import *
from collections import defaultdict

def chooseType(coinType):
    # usdt_btc 转为 btcusdt
    pay = coinType.split("_")[0]
    coin = coinType.split("_")[1]
    return (coin+pay).upper()

class binance:
    def __init__(self,account=""):
        self.account = account
        api_key, secret_key = get_account_key("binance", account)
        self.api = Client(api_key,secret_key)

    def get_tickers(self, coinType, method="ticker"):
        coinType = chooseType(coinType)
        try:
            # params = {"symbol": coinType}
            res = self.api.get_orderbook_ticker(symbol=coinType)
            return {"buyOne": res["bidPrice"], "sellOne": res["askPrice"]} 
        except Exception as e:
            return {"result": "fail", "msg": "%s" % e}
    
    def getAccountInfo(self, method="get_account_info"):
        try:
            res = self.api.get_account()
            res = res["balances"]
            _result = defaultdict(dict)
            for coin in res:
                _result[coin["asset"].lower()]["available"] = float(
                    coin["free"])
                _result[coin["asset"].lower()]["frozen"] = float(
                    coin["locked"])
            return _result
        except Exception as e:
            return {"result": "fail", "msg": "%s" % e}

    def buy(self, coinType, price, amount):
        coinType = chooseType(coinType)
        try:
            res = self.api.create_order(
                timeInForce="GTC",symbol=coinType, side="buy", quantity=amount, price=price, type="LIMIT")
            res["result"] = "success"
            res["id"] = res["orderId"]
            return res
        except Exception as e:
            return {"result": "fail", "msg": "%s" % e}
    def sell(self, coinType, price, amount):
        coinType = chooseType(coinType)
        try:
            res = self.api.create_order(
                timeInForce='GTC', symbol=coinType, side="sell", quantity=amount, price=price, type="LIMIT")
            res["result"] = "success"
            res["id"] = res["orderId"]
            return res
        except Exception as e:
            return {"result": "fail", "msg": "%s" % e}

    def cancelOrder(self, coinType, id):
        coinType = chooseType(coinType)
        try:
            res = self.api.cancel_order(symbol=coinType,orderId=int(id))
            if res["orderId"] == id:
                return {"result": "success", "msg": res}
        except Exception as e:
            return {"result": "fail", "msg": "%s" % e}

    def getOrderInfo(self, coinType, id):
        coinType = chooseType(coinType)
        try:
            res = self.api.get_order(symbol=coinType,orderId=id)
            orderInfo = {}
            orderInfo["id"] = res["orderId"]
            orderInfo["order_price"] = res["price"]
            orderInfo["order_amount"] = res["origQty"]
            if res['status'] == 'filled':
                orderInfo["status"] = "done"
            elif res["status"] == "canceled":
                orderInfo["status"] = "canceled"
            else:
                orderInfo["status"] = "submitted"
            orderInfo["result"] = "success"
        except Exception as e:
            return {"result": "fail", "msg": "%s" % e}
    
    def getOrders(self, coinType):
        coinType = chooseType(coinType)
        try:
            res = self.api.get_open_orders(symbol=coinType)
            orders = []
            for order in res:
                _order = {}
                _order["id"] = order["orderId"]
                _order["price"] = float(order["price"])
                _order["amount"] = float(order["origQty"])
                _order["type"] = "buy" if order["side"] == "BUY" else "sell"
                orders.append(_order)
            return orders
        except Exception as e:
            return {"result": "fail", "msg": "%s" % e}
        
        
if __name__ == '__main__':
    b = binance("huangxinyu")
    b.get_tickers("usdt_btc")

    
    
