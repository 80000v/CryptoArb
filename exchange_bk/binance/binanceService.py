# !/usr/bin/env python
# coding:utf-8

from .binanceClient import *


ACCESS_KEY = ""
SECRET_KEY = ""

client = Client(ACCESS_KEY, SECRET_KEY)


def set_key(_Access, _Secret):
    global ACCESS_KEY, SECRET_KEY, client
    ACCESS_KEY = _Access
    SECRET_KEY = _Secret
    client = Client(ACCESS_KEY, SECRET_KEY)


def chooseType(coinType):
    coinType_map = {
                    1: "USDTETH"
                   }
    if isinstance(coinType, int):
        return coinType_map.get(coinType)
    return coinType

def get_tickers(symbol):
    '''
    :param symbol:  str
    :return: {"buyOne": 0, "sellOne": 0}
    获取不到的时候返回none
    '''
    symbol = chooseType(symbol)
    result = client.get_ticker(symbol=symbol)
    return result


def get_depth_data(symbol):
    """
    :param symbol:
    :return:
    bids 中存放买一到买八的数据。序列中[0]存放price，[1]存放number  以float数值形式。
    asks 存放卖一到卖八 如上
    注意：data['bids][0]为买一  ['asks][0]为卖一
    """
    symbol = chooseType(symbol)
    client = Client(ACCESS_KEY, SECRET_KEY)
    result = client.get_order_book(symbol=symbol, limit=8)
    print(result)

def get_balance_data():
    """
    :return: 返回所有有资产的币种.按下面的形式封装
    """

    return {symbol.lower(): {"frozen": 0, "available": 0 }}


def buy(symbol, price, amount):
    """
    :params symbol: 交易对
    :params price : 买入价格
    :params amount: 买入数量
    :return:
    如果成功返回:
        {"id": order_id,
         "price": price,
         "amount": amount,
         "status": "fail",
         "result": "success"}
    如果失败返回:
        {
        "result": "fail",
        "msg": error
        }
    """
    return 

def sell(symbol, price, amount):
    """
    :params symbol: 交易对
    :params price : 买入价格
    :params amount: 买入数量
    :return:
    如果成功返回:
        {"id": order_id,
         "price": price,
         "amount": amount,
         "status": "fail",
         "result": "success"}
    如果失败返回:
        {
        "result": "fail",
        "msg": error
        }
    """
    return 

def orderBook(symbol):
    """ 如果获取失败。返回None"""
    return {"bids": [{"price": 1, "amount": 1},...],
            "asks": [{"price": 1.1, "amount": 1},...]}

# if __name__ == '__main__':
#     get_depth_data("USDTBTC")
#     get_tickers("USDTBTC")
