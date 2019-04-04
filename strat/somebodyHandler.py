# !/usr/bin/env python
# coding:utf-8
import sys
sys.path.append("../../crossexchangearb")

# 添加交易所
#---------------------------------------
from exchange import *
from mainHandler import MainHandler

# 常用的库
#---------------------------------------
import time

# 同时开多个交易对
#trade_coin = ["usdt_neo", "usdt_xrp"]
trade_coin = ["usdt_eth"]


def start():
    for symbol in trade_coin:
        mh = MainHandler(symbol,account="huangxinyu")
        mh.start()
        time.sleep(3)


if __name__ == '__main__':
  while True:
    start()
