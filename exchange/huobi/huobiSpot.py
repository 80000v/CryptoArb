#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-16 15:40:03
# @Author  : Ryan (tech@huobi.com)
# @Link    : https://www.huobi.com
# @Version : $Id$

from Util import *

'''
Market data API
'''


# 获取KLine
def get_kline(symbol, period, size=100, account=None):
    """
    :param symbol: 可选值：{ ethcny }
    :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param long_polling: 可选值： { true, false }
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size,
              "account": account}

    # if long_polling:
    #     params['long-polling'] = long_polling
    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)


# 获取marketdepth
def get_depth(symbol, type, long_polling=None, account=None):
    """
    :param symbol: 可选值：{ ethcny }
    :param type: 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
    :param long_polling: 可选值： { true, false }
    :return:
    """
    params = {'symbol': symbol,
              'type': type,
              "account": account}

    if long_polling:
        params['long-polling'] = long_polling
    url = MARKET_URL + '/market/depth'
    return http_get_request(url, params)


# 获取tradedetail
def get_trade(symbol, long_polling=None, account=None):
    """
    :param symbol: 可选值：{ ethcny }
    :param long_polling: 可选值： { true, false }
    :return:
    """
    params = {'symbol': symbol, "account": account}
    if long_polling:
        params['long-polling'] = long_polling
    url = MARKET_URL + '/market/trade'
    return http_get_request(url, params)


# 获取 Market Detail 24小时成交量数据
def get_detail(symbol, long_polling=None, account=None):
    """
    :param symbol: 可选值：{ ethcny }
    :param long_polling: 可选值： { true, false }
    :return:
    """
    params = {'symbol': symbol, "account": account}
    if long_polling:
        params['long-polling'] = long_polling
    url = MARKET_URL + '/market/detail'
    return http_get_request(url, params)


'''
Trade/Account API
'''


def get_accounts(account=None):
    """
    :return: 
    """
    path = "/v1/account/accounts"
    params = {"account": account}
    return api_key_get(params, path)


# 获取当前账户资产
def get_balance(acct_id=None, account=None):
    """
    :param acct_id
    :return:
    """

    if not acct_id:
        accounts = get_accounts(account=account)
        acct_id = accounts['data'][0]['id']

    url = "/v1/account/accounts/{0}/balance".format(acct_id)
    params = {"account-id": acct_id, "account": account}
    return api_key_get(params, url)


# 下单
def orders(amount, source, symbol, _type, price=0, account=None):
    """
    
    :param amount: 
    :param source: 
    :param symbol: 
    :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param price: 
    :return: 
    """
    accounts = get_accounts()
    acct_id = accounts['data'][0]['id']

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": source,
              "account": account}
    if price:
        params["price"] = price

    url = "/v1/order/orders"
    return api_key_post(params, url)


# 执行订单
def place_order(order_id, account=None):
    """
    
    :param order_id: 
    :return: 
    """
    params = {"account": account}
    url = "/v1/order/orders/{0}/place".format(order_id)
    return api_key_post(params, url)


# 撤销订单
def cancel_order(order_id, account=None):
    """
    
    :param order_id: 
    :return: 
    """
    params = {"account": account}
    url = "/v1/order/orders/{0}/submitcancel".format(order_id)
    return api_key_post(params, url)


# 查询某个订单
def order_info(order_id, account=None):
    """
    
    :param order_id: 
    :return: 
    """
    params = {"account": account}
    url = "/v1/order/orders/{0}".format(order_id)
    return api_key_get(params, url)


# 查询某个订单的成交明细
def order_matchresults(order_id, account=None):
    """
    
    :param order_id: 
    :return: 
    """
    params = {"account": account}
    url = "/v1/order/orders/{0}/matchresults".format(order_id)
    return api_key_get(params, url)


# 查询当前委托、历史委托
def orders_list(symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None, account=None):
    """
    
    :param symbol: 
    :param states: 可选值 {pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}
    :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: 可选值{prev 向前，next 向后}
    :param size: 
    :return: 
    """
    params = {'symbol': symbol,
              'states': states,
              "account": account}

    if types:
        params["types"] = types
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
    return api_key_get(params, url)


# 查询当前成交、历史成交
def orders_matchresults(symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None, account=None):
    """
    
    :param symbol: 
    :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: 可选值{prev 向前，next 向后}
    :param size: 
    :return: 
    """
    params = {'symbol': symbol, "account": account}

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
    url = '/v1/order/matchresults'
    return api_key_get(params, url)


# 查询虚拟币提现地址
def get_withdraw_address(currency, account=None):
    """
    
    :param currency: 
    :return: 
    """
    params = {'currency': currency, "account": account}
    url = '/v1/dw/withdraw-virtual/addresses'
    return api_key_get(params, url)


def query_withdraw(currency, start_id, size, account=None):
  params = {}
  if start_id == "":
    params = {'currency': currency, 'type': 'withdraw', 'from':'0', 'size':'100', 'account':account}
  else:
    params = {'currency': currency, 'type': 'withdraw', 'from':'0', 'size':str(size), 'id':str(start_id), 'account':account}
  #print params
  url='/v1/query/deposit-withdraw'
  return api_key_get(params, url)

# 申请提现虚拟币
def withdraw(address, amount, currency, fee=None, addr_tag=None,account=None):
    """
    :param address: 
    :param amount: 
    :return: 
    """
    params = {'address': address,
              'amount': amount,
              "currency": currency,
              "account": account}
    if fee:
        params["fee"] = fee
    if addr_tag:
        params["addr-tag"] = addr_tag
    url = '/v1/dw/withdraw/api/create'
    print params
    return api_key_post(params, url)


# 确认申请虚拟币提现
def place_withdraw(address_id, account=None):
    """
    
    :param address_id: 
    :return: 
    """
    params = {}
    url = '/v1/dw/withdraw-virtual/{0}/place'.format(address_id)
    return api_key_post(params, url)


# 申请取消提现虚拟币
def cancel_withdraw(address_id, account=None):
    """
    
    :param address_id: 
    :return: 
    """
    params = {"account": account}
    url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)
    return api_key_post(params, url)

if __name__ == '__main__':
    print get_accounts()
    print get_balance()
    print get_trade("etcbtc")
