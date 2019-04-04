#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-18 17:40:03
# @Author  : 
# @Link    : https://www.huobi.com
# @Version : $$$1.0$$$

import huobiSpot as nh
import httplib
import json
import urlparse
import time
from collections import defaultdict

def chooseType(coinType):
    # usdt_btc 转为 btcusdt
    pay = coinType.split("_")[0]
    coin = coinType.split("_")[1]
    return coin+pay

class huobi:
    
    def __init__(self,account=""):
        self.account = account

    def get_trade_params(self, price, amount, coinType, method):
        params = {}
        accounts = nh.get_accounts(account=self.account)
        acct_id = accounts['data'][0]['id']
        params['account-id'] = acct_id
        params["amount"] = amount
        params["symbol"] = coinType
        params["type"] = method
        params["price"] = price
        params["source"] = "api"
        params["account"] = self.account
        return params


    def get_tickers(self,coinType, method="ticker"):
        coinType = chooseType(coinType)
        market_url = urlparse.urlparse(nh.MARKET_URL).hostname
        try:
            conn = httplib.HTTPConnection(market_url, timeout=2)
            conn.request('GET', '/market/detail/merged?symbol=%s' % coinType)
            ticker = json.loads(conn.getresponse().read())
            _result = {"buyOne": ticker["tick"]["bid"]
                    [0], "sellOne": ticker["tick"]["ask"][0]}
            return _result
        except Exception as e:
            return {"result": "fail", "msg": "%s" % e}


    def getAccountInfo(self,method="get_account_info"):
        try:
            result = nh.get_balance(account=self.account)
            # return result
            if result and result["status"] == "ok":
                result = result["data"]["list"]
            if not result:
                return {"result": "fail", "msg": "%s" % result}
            _result = defaultdict(dict)
            for coin in result:
                if coin["type"] == "trade":
                    _result[coin["currency"]]["available"] = float(coin["balance"])
                if coin["type"] == "frozen":
                    _result[coin["currency"]]["frozen"] = float(coin["balance"])
            if "qtum" not in _result:
                _result["qtum"] = {"available": 0, "frozen": 0}
            return _result
        except BaseException as e:
            return {"result": "fail", "msg": "%s" % e}


    def buy(self,coinType, price, amount, method="buy-limit"):
        coinType = chooseType(coinType)
        path = '/v1/order/orders/place'
        params = self.get_trade_params(price, amount, coinType, method)
        try:
            result = nh.api_key_post(params, path)
            if result and result["status"] == "ok":
                result["result"] = "success"
                result["id"] = result["data"]
                return result
        except BaseException as e:
            return {"result": "fail", "msg": "%s" % e}
        return {"result": "fail", "msg": json.dumps(result) if result else ""}


    def sell(self,coinType, price, amount, method="sell-limit"):
        coinType = chooseType(coinType)
        path = '/v1/order/orders/place'
        params = self.get_trade_params(price, amount, coinType, method)
        try:
            result = nh.api_key_post(params, path)
            if result and result["status"] == "ok":
                result["result"] = "success"
                result["id"] = result["data"]
                return result
        except BaseException as e:
            return {"result": "fail", "msg": "%s" % e}
        return {"result": "fail", "msg": json.dumps(result) if result else ""}


    def cancelOrder(self,coinType, id, method="cancel_order"):
        coinType = chooseType(coinType)
        params = {"account":self.account}
        url = "/v1/order/orders/{0}/submitcancel".format(id)
        result = nh.api_key_post(params, url)
        if result and result["status"] == "ok":
            result["result"] = "success"
            return result
        return {"result": "fail", "msg": result}


    def getOrderInfo(self,coinType, id, method="order_info"):
        # pre-submitted 准备提交, submitting , submitted 已提交, partial-filled 部分成交,
        # partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销
        coinType = chooseType(coinType)
        path = '/v1/order/orders/%s' % id
        params = {"account": self.account}
        result = nh.order_info(id)
        if result and result['status'] == 'ok':
            orderInfo = {}
            result = result["data"]
            orderInfo["id"] = result["id"]
            orderInfo["order_price"] = result["price"]
            orderInfo["order_amount"] = result["amount"]
            orderInfo["type"] = chooseType_num(result["symbol"])

            if result['state'] == 'filled':
                orderInfo["status"] = 2
            elif result["state"] == "canceled":
                orderInfo["status"] = 3
            else:
                orderInfo["status"] = 7
            orderInfo["result"] = "success"
            return orderInfo
        return {"result": "fail"}


    def getOrders(self,coinType, states="submitted", types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
        coinType = chooseType(coinType)
        params = {'symbol': coinType,
                'states': states,
                "account": self.account}

        if types:
            params[types] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/orders'
        result = nh.orders_list(params, url)
        if result and result["status"] == "ok":
            _result = []
            for order in result["data"]:
                _order = {}
                _order["id"] = order["id"]
                _order["price"] = float(order["price"])
                _order["amount"] = float(order["amount"])
                # type:交易类型 0 限价买 1 限价卖 不搞市价下单，不好控制
                _order["type"] = 0 if order["type"] == "buy-limit" else 1
                # status:0未成交　1部分成交　2已完成　3已取消
                # _order["status"] = 0
                _result.append(_order)
            return _result
        return []


    def getKline(self,coinType, period, size):
        coinType = chooseType(coinType)
        result = nh.get_kline(coinType, period, size)
        if result and result["status"] == "ok":
            return result["data"][::-1]
        return {}

    def withdraw(self, currency, address, amount, fee=None, addr_tag=None):
        result = nh.withdraw(address, amount,currency,fee,addr_tag=addr_tag, account=self.account)
        if result and result["status"] == "ok":
            return {"result": "success", "msg": result["data"]}
        return {"result": "fail", "msg": result}



if __name__ == '__main__':
    a = huobi(account="huangxinyu")
    print a.buy("usdt_btc",6.25,0.01)
    # getKline(5,"15min",100)
    # print getOrders(5)
    # print get_tickers(5)
    # print getOrderInfo(5, 3895172944)
    # print getAccountInfo()
    # print nh.get_accounts()
