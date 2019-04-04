#!/usr/bin/python
# -*- coding: utf-8 -*-
# 用于访问OKCOIN 现货REST API
from HttpMD5Util import buildMySign, httpGet, httpPost

apikey = ''
secretkey = ''


class OKCoinSpot:

    def __init__(self, url, apikey, secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    # 获取OKCOIN现货行情信息
    def ticker(self, symbol=''):
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return httpGet(self.__url, TICKER_RESOURCE, params)

    # 资金划转
    def funds_transfer(self, amount, From, To, symbol=""):
        # 转出账户(1：币币账户 3：合约账户 6：我的钱包)
        USERINFO_RESOURCE = "/api/v1/funds_transfer.do"
        params = {'api_key': self.__apikey,
                  "symbol": symbol,
                  "amount": amount,
                  "from": From,
                  "to": To}
        params['sign'] = buildMySign(params, self.__secretkey)
        #print params
        return httpPost(self.__url, USERINFO_RESOURCE, params)

    # 获取OKCOIN现货市场深度信息
    def depth(self, symbol=''):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return httpGet(self.__url, DEPTH_RESOURCE, params)

    # 获取OKCOIN现货历史交易信息
    def trades(self, symbol=''):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return httpGet(self.__url, TRADES_RESOURCE, params)

    def walletinfo(self):
        WALLETINFO_RESOURCE = "/api/v1/wallet_info.do"
        params = {}
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, WALLETINFO_RESOURCE, params)

    # 获取用户现货账户信息
    def userinfo(self):
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params = {}
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, USERINFO_RESOURCE, params)

    # 现货交易
    def trade(self, symbol, tradeType, price='', amount=''):
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'type': tradeType
        }
        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount

        params['sign'] = buildMySign(params, self.__secretkey)
        print params
        return httpPost(self.__url, TRADE_RESOURCE, params)

    # 现货批量下单
    def batchTrade(self, symbol, tradeType, orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'type': tradeType,
            'orders_data': orders_data
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, BATCH_TRADE_RESOURCE, params)

    # 现货取消订单
    def cancelOrder(self, symbol, orderId):
        CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, CANCEL_ORDER_RESOURCE, params)

    # 现货订单信息查询
    def orderinfo(self, symbol, orderId):
        ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDER_INFO_RESOURCE, params)

    def query_withdraw(self, currency, id):
        QUERY_WITHDRAW_RESOURCE = '/api/v1/withdraw_info.do'
        params = {
            'api_key': self.__apikey,
            'symbol': currency,
            'withdraw_id': id
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        #print params
        return httpPost(self.__url, QUERY_WITHDRAW_RESOURCE, params)

    # 现货批量订单信息查询
    def ordersinfo(self, symbol, orderId, tradeType):
        ORDERS_INFO_RESOURCE = "/api/v1/orders_info.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'order_id': orderId,
            'type': tradeType
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDERS_INFO_RESOURCE, params)

    # 现货获得历史订单信息
    def orderHistory(self, symbol, status, currentPage, pageLength):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'status': status,
            'current_page': currentPage,
            'page_length': pageLength
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDER_HISTORY_RESOURCE, params)

    def withdraw(self, symbol, withdraw_address, withdraw_amount, trade_pwd, chargefee, target):
        '''
        提币BTC/LTC/ETH/ETC/BCH
        :param symbol:btc_usd:比特币    ltc_usd :莱特币    eth_usd :以太坊     etc_usd :以太经典    bch_usd :比特现金
        :param withdraw_address:认证的地址、邮箱 或手机号码
        :param withdraw_amount:提币数量 BTC>=0.01 LTC>=0.1 ETH>=0.1 ETC>=0.1 BCH>=0.1
        :param trade_pwd:交易密码
        :param chargefee:网络手续费 >=0
                        BTC范围 [0.002，0.005]
                        LTC范围 [0.001，0.2]
                        ETH范围 [0.01]
                        ETC范围 [0.0001，0.2]
                        BCH范围 [0.0005，0.002]
                        手续费越高，网络确认越快，OKCoin内部提币设置0
        :param target:地址类型 okcn：国内站 okcom：国际站 okex：OKEX address：外部地址
        :return:
        '''
        path = "/api/v1/withdraw.do"
        params = {'api_key': self.__apikey,
                  'symbol': symbol,
                  'withdraw_address': withdraw_address,
                  'withdraw_amount': withdraw_amount,
                  'trade_pwd': trade_pwd,
                  'chargefee': chargefee,
                  'target': "address"
                  }
        print params
        params['sign'] = buildMySign(params, self.__secretkey)
        #print params
        return httpPost(self.__url, path, params)