#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
# 客户端调用，用于查看API返回结果

# 现货
# from OkcoinFutureAPI import OKCoinFuture
import requests
import httplib
import urlparse
import json
from collections import defaultdict
import time
# 期货的
from OkcoinFutureAPI import OKCoinFuture
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

append_path = '../../strategy'
sys.path.append(append_path)

from util.general import *

# 初始化apikey，secretkey,url
# apikey = '7033039d-0a60-4c6a-9758-7d18eb724d36'
# secretkey = '3A82A8B5D1988704DC2BB7885483A568'
okcoinRESTURL = 'https://www.okex.com'


class OKEXFutureService(object):

    def __init__(self, account=None):
        self.account = account

    def chooseType(self, coinType):
        if isinstance(coinType, int):
            if coinType == 3:
                coinType = 'etc_btc'
            elif coinType == 4:
                coinType = 'eth_btc'
            elif coinType == 5:
                coinType = 'etc_usdt'
            elif coinType == 6:
                coinType = 'eth_usdt'
            elif coinType == 7:
                coinType = 'btc_usdt'
            elif coinType == 8:
                coinType = 'qtum_usdt'
            elif coinType == 9:
                coinType = 'eos_usdt'
            elif coinType == 10:
                coinType = 'omg_usdt'
            elif coinType == 11:
                coinType = 'ltc_usdt'
            elif coinType == 12:
                coinType = 'bch_usdt'
        return coinType

    def chooseType_num(self, coinType):
        if isinstance(coinType, str):
            try:
                _invert = {}
                for i in range(12):
                    _invert[self.chooseType(i)] = i
                return _invert[coinType]
            except:
                return coinType
        return coinType

    def get_position_params(self, contractType, coinType, type1):
        params = {}
        params["contractType"] = contractType
        params["symbol"] = coinType
        params["type"] = type1
        return params

    def get_trade_params(self, coinType, price, amount, tradeType):
        params = {}
        # 先使用固定参数
        params["lever_rate"] = 10

        # 执行参数
        params["symbol"] = coinType
        params["type"] = tradeType
        params["amount"] = amount
        params["price"] = price

        return params

    '''
    获取账号详情
    '''

    def getAccountInfo(self, method="future_userinfo_4fix"):
        result = self.api_get(method="future_userinfo_4fix")
        if result and result["result"] == True:
            result = result["info"]
            _result = {}
            for coin in result:
                _result[coin] = {
                    "available": float(result[coin]["rights"])
                }
                if result[coin]["contracts"]:
                    _result[coin].update({
                        "unprofit": result[coin]["contracts"][0]["unprofit"],
                        "profit": result[coin]["contracts"][0]["profit"]
                    })
            return _result
        return {"result": "fail"}

    def getPosition(self, coinType, contractType="this_week", method="future_position_4fix"):
        coinType = self.chooseType(coinType)
        type1 = 1
        params = self.get_position_params(contractType, coinType, type1)
        result = self.api_get(method, params)
        # return result
        if result and result["result"] == True:
            result = result["holding"]
            _result = {}
            # print result
            for i in result:
                _result[i["symbol"]] = {
                    "sell": {
                        "ratio": float(i['sell_profit_lossratio']),
                        "avg_price": i['sell_price_avg'],
                        "amount": i["sell_amount"],
                        "boom": float(i["sell_flatprice"])
                    },
                    "buy": {
                        "ratio": float(i['buy_profit_lossratio']),
                        "avg_price": i['buy_price_avg'],
                        "amount": i["buy_amount"],
                        "boom": float(i["buy_flatprice"])
                    }
                }
            return _result
        return None

    def get_tickers(self, coinType, contractType="this_week", method="ticker"):
        coinType = self.chooseType(coinType)
        market_url = urlparse.urlparse(okcoinRESTURL).hostname
        try:
            conn = httplib.HTTPSConnection(market_url, timeout=2)
            conn.request('GET', '/api/v1/future_ticker.do?symbol=%s&contract_type=%s' % (coinType, contractType))
            result = json.loads(conn.getresponse().read())
            if result and result.has_key("ticker"):
                _result = {}
                _result["buyOne"] = result["ticker"]["buy"]
                _result["sellOne"] = result["ticker"]["sell"]
                _result["high"] = result["ticker"]["high"]
                _result["low"] = result["ticker"]["low"]
            return _result
        except Exception as e:
            print e
            return {"result": "fail", "msg": "%s" % e}

    def trade(self, coinType, price, amount, tradeType, match_price=None, contractType="this_week", method="trade"):
        # tradeType 1:开多   2:开空   3:平多   4:平空
        # this_week:当周   next_week:下周   quarter:季度
        coinType = self.chooseType(coinType)
        params = self.get_trade_params(coinType, price, amount, tradeType)
        if match_price:
            params["match_price"] = 1
        else:
            params['match_price'] = 0
        params["contractType"] = contractType
        result = self.api_get(method, params)
        if result and result["result"] == True:
            return {"result": "success", "id": result["order_id"]}
        return {"result": "fail", "msg": result}

    def cancelOrder(self, coinType, id, contractType="next_week", method="cancelOrder"):
        coinType = self.chooseType(coinType)
        params = {"symbol": coinType, "id": id, "contractType": contractType}
        result = self.api_get(method, params)
        print result
        if result and result["result"] == True:
            return {"result": "success", "id": result["order_id"]}
        return {"result": "fail"}

    def getOrderInfo(self, coinType, id, contractType='next_week', method="order_info"):
        '''
        status: 订单状态(0等待成交 1部分成交 2全部成交 -1撤单 4撤单处理中 5撤单中)
        type 1:开多   2:开空   3:平多   4:平空
        '''
        coinType = self.chooseType(coinType)
        params = {"symbol": coinType, "id": id, "contractType": contractType}
        result = self.api_get(method, params)
        if result and result["result"] == True:
            if not result["orders"]:
                return {"result": "fail", "msg": "empty message"}
            orderInfo = result["orders"][0]
            _result = {"result": "success"}
            _result["id"] = orderInfo["order_id"]
            _result["price"] = orderInfo["price"]
            _result["amount"] = orderInfo["amount"]
            _result["status"] = orderInfo["status"]
            _result["type"] = orderInfo["type"]
            return _result
        return {"result": "fail", "msg": result}

    def api_get(self, method, params={}):
        # 现货API
        if self.account:
            apikey, secretkey = get_account_key("okex", self.account)
        okcoinSpot = OKCoinFuture(okcoinRESTURL, apikey, secretkey)
        if method == "future_userinfo_4fix":
            api_do = "okcoinSpot.%s()" % (method)
            return eval(api_do)

        elif method == "future_position_4fix":
            return okcoinSpot.future_position_4fix(params["symbol"], params["contractType"], params["type"])

        elif method == "trade":
            return okcoinSpot.future_trade(params["symbol"],
                                           params["contractType"],
                                           params["price"],
                                           params["amount"],
                                           params["type"],
                                           params["match_price"],
                                           params["lever_rate"])

        elif method == "ticker":
            return okcoinSpot.future_ticker(params["symbol"], params["contractType"])

        elif method == "order_info":
            return okcoinSpot.future_orderinfo(params["symbol"], params["contractType"], params["id"])

        elif method == "cancelOrder":
            return okcoinSpot.future_cancel(params["symbol"], params["contractType"], params["id"])


if __name__ == '__main__':
    # trade(9,8.24,1,1)
    ok = OKEXFutureService("wanghuageng")
    print ok.get_tickers(9)
    print ok.getAccountInfo()
    # print getPosition(9)
    # print getOrderInfo(9,1040492596114432, contractType="this_week")
    # print trade(9, 7,1,1)
    # print cancelOrder(9, 1035794044242944, contractType="this_week")
