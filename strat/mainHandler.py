# !/usr/bin/env python
# coding:utf-8


import sys
sys.path.append("../../crossexchangearb")

# 交易所
#---------------------------------------
from exchange import *

# 常用工具
#---------------------------------------
from util import util as u
import json
import  httplib
import time

# 加载配置
#---------------------------------------
from ConfigParser import ConfigParser
CF = ConfigParser()
CF.read("../config/arb.ini")

def chooseType(coinType):
    # usdt_btc 转为 btcusdt
    pay = coinType.split("_")[0]
    coin = coinType.split("_")[1]
    return coin+pay


class MainHandler(object):

    def __init__(self, coinType, account=""):
        self.coinType = coinType
        self.account = account
        self.strCoinType = coinType
        self.pay = self.strCoinType.split("_")[0].lower()
        self.coin = self.strCoinType.split("_")[1].lower()
        self.amount = CF.getfloat(self.strCoinType, "amount")
        self.base_bit = CF.getfloat(self.strCoinType, "base_bit")
        self.profit_bit = CF.getfloat(self.strCoinType, "profit_bit")
        self.PROFIT = CF.getfloat(self.strCoinType, "profit")
        self.stop_sell_out_count = CF.getfloat(
            self.strCoinType, "sell_out_count")
        self.stop_buy_back_count = CF.getfloat(
            self.strCoinType, "buy_back_count")
        self.dynamic_amount = CF.getfloat(self.strCoinType, "dynamic_amount")
        self.status = CF.get(self.strCoinType, "status")
        self.exchange = json.loads(CF.get(self.strCoinType, "exchanges"))
        self.withdraw_address = eval(CF.get(self.strCoinType, "withdraw_address"))
        self.withdraw_tag = eval(CF.get(self.strCoinType, "withdraw_tag"))
        self.min_withdraw_amount = eval(CF.get(self.strCoinType, "min_withdraw_amount"))
        self.withdraw_fee = eval(CF.get(self.strCoinType, "withdraw_fee"))
        self.withdraw_map = {}
        self.withdraw_ex_map = {}
        self.pre_allCoin = 0.0
        self.fee = eval(CF.get(self.strCoinType, "fee"))
        self.buy_withdraw_point = eval(CF.get(self.strCoinType, "buy_withdraw_point"))
        self.is_buy_transfer = False

    def HandleMsg(self, exchange, wid, msg):
      if exchange == "huobi":
        if msg['result'] == "success":
          content = msg['msg']
          for c in content:
            qid = c['id']
            s = c['state']
            if str(qid) == str(wid) and s == "confirmed":
              print exchange + " transfer finished!"
              if withdraw_ex_map[exchange] == 'okex':
                re = eval("self.okex").funds_transfer(self.coin, self.min_withdraw_amount[exchange], "6", "1")
                if re['result'] != 'success':
                  print "withdraw to okex finsihed, but transfer failed " + str(re)
                  return False
                
              self.count_all()
              if ((self.pre_allCoin-self.allCoin)/self.allCoin < 0.01):
                print str(self.allCoin) + "->" + str(self.pre_allCoin)
                del self.withdraw_map[str(ex)]
                del self.withdraw_ex_map[str(ex)]
                return True
              else:
                print "transfer error, total coin reduce from %d->%d" %(exchange, self.pre_allCoin, self.allCoin)
              return False
          return False
        else:
          print exchange + " query withdraw failed " + str(wid)
          return False

      elif exchange == "okex":
        #print msg
        #{'msg': {u'result': True, u'withdraw': [{u'status': 0, u'target': u'', u'address': u'r4t2K7yKHvQ1RmznNssRRv6QMTBw8uDZQ7:107250', u'chargefee': 0.15, u'amount': 20.1, u'created_date': 1535966106000, u'withdraw_id': 1800043}]}, 'result': 'success'}
        if msg['result'] == "success":
          content = msg['msg']
          # {u'result': True, u'withdraw': [{u'status': -2, u'target': u'okcoin.com', u'address': u'0979524648', u'chargefee': 0.0, u'amount': 0.224, u'created_date': 1535942147000, u'withdraw_id': 1798111}]}
          if content['result'] == True:
            wcontent = content['withdraw'][0]
            qid = wcontent['withdraw_id']
            s = wcontent['status']
            print "line 90 " + str(qid) + str(wid) + " state is " + str(s)
            if str(qid) == str(wid) and str(s) == "2":
              print exchange + "transfer finished!"
              #re = eval("self."+exchange).funds_transfer(self.coin, self.min_withdraw_amount[exchange], "6", "1")
              #if re['result'] != 'success':
                #print "withdraw finsihed, but transfer failed " + str(re)
                #return False
                
              self.count_all()
              if ((self.pre_allCoin-self.allCoin)/self.allCoin < 0.01):
                print str(self.allCoin) + "->" + str(self.pre_allCoin)
                del self.withdraw_map[str(exchange)]
                del self.withdraw_ex_map[str(exchange)]
                return True
              else:
                print "%s transfer error, total coin reduce from %d->%d" %(exchange, self.pre_allCoin, self.allCoin)
              return False
            #return False
            time.sleep(10)
          else:
            print "msg failed, "+ str(content)
            return False
        else:
          print exchange + " query withdraw failed " + str(wid)
          return False
      else:
        print exchange + "not found"
              
  
    def count_all(self):
        self.e_balance = {}
        for e in self.exchange:
            try:
                self.e_balance[e] = eval("self." + e + ".getAccountInfo()")
                if self.e_balance[e]['status'] == "fail":
                  print "countall failed"
                  return False
            except BaseException as b:
                print "getAccountInfo error: %s :%s" % (e, b)
                return False

        self.allCoin, self.allPay = 0, 0
        if len(self.e_balance) == len(self.exchange):
            for e in self.e_balance:
                self.allPay += self.e_balance[e][self.pay]["frozen"] + \
                    self.e_balance[e][self.pay]["available"]
                self.allCoin += self.e_balance[e][self.coin]["frozen"] + \
                    self.e_balance[e][self.coin]["available"]

        print "coin account: %s" % self.allCoin
        print "paycoin account: %s" % self.allPay
        if self.stop_buy_back_count < self.allCoin or self.allCoin < self.stop_sell_out_count:
            print "coincount error. %s" % self.allCoin
            return False
        return True

    def get_tickers(self):
        _result = {}
        for e in self.exchange:
            #import pdb;pdb.set_trace()
            ticker = eval("self." + e + ".get_tickers('%s')" % self.coinType)
            if ticker:
                _result[e] = ticker

        return _result

    def get_last_price(self):
        try:
            conn = httplib.HTTPConnection(r'api.huobi.pro', timeout=2)
            conn.request('GET', "/market/detail/merged?symbol=%s" %
                         chooseType(self.coinType))
            huobi_ticker = json.loads(conn.getresponse().read())
            _result = huobi_ticker["tick"]["close"]
            return float(_result)
        except Exception as e:
            print "get_last_price Error:", e
            return None

    def main(self):
        can_continue = self.count_all()
        if not can_continue:
            return
        #import pdb;pdb.set_trace()
        tickers = self.get_tickers()
        print("ticker is ", str(tickers))
        for e in tickers:
          if "buyOne" not in tickers[e] or "sellOne" not in tickers[e]:
            print "Network fail"
            return
        if not tickers:
            return
        if len(tickers) < 2:
            return

        createVar = self.__dict__
        bo_list, so_list = {}, {}
        for e in self.exchange:
            createVar[e+"_bo"] = 0
            createVar[e+"_so"] = 0

            if tickers.has_key(e):
                createVar[e+"_bo"] = float(tickers[e]["buyOne"])
                createVar[e+"_so"] = float(tickers[e]["sellOne"])

            bo_list[e+"_bo"] = createVar[e+"_bo"]
            so_list[e+"_so"] = createVar[e+"_so"]

        for price in bo_list:
            for _price in so_list:
                sell_exchange = price.split("_")[0]
                buy_exchange = _price.split("_")[0]
                if sell_exchange == buy_exchange:
                    continue
                if sell_exchange not in self.e_balance:
                    continue
                if buy_exchange not in self.e_balance:
                    continue
                if bo_list[price] and so_list[_price]: # and bo_list[price] > so_list[_price]:
                    print price, " - ", _price, ": ", bo_list[price] - so_list[_price]
                    print "profitable spread: ", self.profit
                    if bo_list[price] and so_list[_price] and bo_list[price] - so_list[_price] >= self.profit:
                        #self.count_orderbook(
                            #sell_exchange, buy_exchange, bo_list[price], so_list[_price])
                        if float(self.e_balance[sell_exchange][self.coin]["available"]) < self.amount: # sell coin not enough
                           print "%s is not enough in %s: avail %s, sell amount %lf" %(self.coin,
                                  sell_exchange, self.e_balance[sell_exchange][self.coin]["available"], self.amount)
                           if float(self.e_balance[buy_exchange][self.coin]["available"]) >= self.min_withdraw_amount[buy_exchange]:
                             # enough coin in the other exchange
                             print "transfer from %s: coin reduce %lf -> %lf" %(buy_exchange,
                                   float(self.e_balance[buy_exchange][self.coin]["available"]),
                                   float(self.e_balance[buy_exchange][self.coin]["available"])-self.min_withdraw_amount[buy_exchange])
                             be = eval("self." + buy_exchange)
                             total_coin = self.allCoin
                             transfer_req = be.withdraw(currency=self.coin, address=self.withdraw_address[sell_exchange], amount=self.min_withdraw_amount[buy_exchange], addr_tag=self.withdraw_tag[sell_exchange], fee = self.withdraw_fee[buy_exchange])
                             print transfer_req
                             if transfer_req["result"] == "success":
                               self.pre_allCoin = total_coin
                               print "transfer request send success, pre coin " + str(total_coin)
                               d = eval(transfer_req['msg'])
                               if d.has_key('withdraw_id'):
                                 self.withdraw_map[buy_exchange]=d['withdraw_id']
                                 print "register %s = %s" %(buy_exchange, str(d['withdraw_id']))
                                 self.withdraw_ex_map[buy_exchange]=sell_exchange
                               else:
                                 self.withdraw_map[buy_exchange]=d
                                 print "register %s = %s" %(buy_exchange, str(d))
                                 self.withdraw_ex_map[buy_exchange]=sell_exchange
                               #print "line229 " + str(transfer_req['msg'])
                               return
                             else:
                               print "transfer request failed"
                               return

                           if float(self.e_balance[buy_exchange][self.pay]["available"]) >= (self.min_withdraw_amount[buy_exchange]+self.buy_withdraw_point[buy_exchange])*so_list[_price]:
                             #no enough coin, buy and transfer right now
                             print "buy from %s, transfer to %s" %(buy_exchange, sell_exchange)
                             #buy:buy_exchange, tranfer
                             be = eval("self." + buy_exchange)
                             br = be.buy(self.coinType, so_list[_price]+0.1, self.min_withdraw_amount[buy_exchange]+self.buy_withdraw_point[buy_exchange])
                             if br['result'] == 'success':
                               time.sleep(1)
                               self.is_buy_transfer = True
                               coin_num = self.allCoin
                               bwr = be.withdraw(currency=self.coin, address=self.withdraw_address[sell_exchange], amount=self.min_withdraw_amount[buy_exchange])
                               print bwr
                               if bwr["result"] == "success":
                                 self.pre_allCoin = coin_num
                                 print "transfer request send success, pre coin " + str(coin_num)
                                 d = eval(bwr['msg'])
                                 if d.has_key('withdraw_id'):
                                   self.withdraw_map[buy_exchange]=d['withdraw_id']
                                   print "register %s = %s" %(buy_exchange, str(d['withdraw_id']))
                                   self.withdraw_ex_map[buy_exchange]=sell_exchange
                                 else: 
                                   self.withdraw_map[buy_exchange]=d
                                   print "register %s = %s" %(buy_exchange, str(d))
                                   self.withdraw_ex_map[buy_exchange]=sell_exchange
                                 return
                               else: 
                                 print 'buy %s in %s success, but transfer failed msg is %s' %(self.coin, buy_exchange, str(bwr))
                                 sys.exit(1)
                                 return
                               
                               #if bwr["result"] == "success":
                                 #return
                               #else:
                                 #print 'buy %s in %s success, but transfer failed msg is %s' %(self.coin, buy_exchange, str(bwr))
                                 #sys.exit(1)
                                 #return
                             else:
                               print "programe want to buy in %s, then transfer to %s, but buy faile, msg is %s" %(buy_exchange, sell_exchange, str(br))
                               return
                           else:
                             print "%s no enough coin to sell even consider withdraw" %(sell_exchange)
                             return

                        #if float(self.e_balance[buy_exchange][self.pay]["available"]) < (bo_list[price])*self.amount:
                           #print "%s is not enough in %s: avail %s, sell amount %lf"  %(self.pay, buy_exchange,
                                  #self.e_balance[buy_exchange][self.pay]["available"], (bo_list[price])*self.amount)
                           #if float(self.e_balance[sell_exchange][self.pay]["available"]) >= self.amount*bo_list[price]:
                             # enough pay in the other exchange
                             #print "transfer from %s: pay reduce %lf -> %lf" %(sell_exchange,
                                   #float(self.e_balance[sell_exchange][self.pay]["available"]),
                                   #float(self.e_balance[sell_exchange][self.pay]["available"])-self.amount*bo_list[price])
                             #se = eval("self." + sell_exchange)
                             #if se.withdraw(currency=self.pay, address=self.withdraw_address[sell_exchange], amount=self.min_withdraw_amount[sell_exchange])["result"] == "success":
                               #is_trans = True
                               #return
                           #else:
                             #print "%s no enough coin to buy even consider withdraw" %(buy_exchange)
                             #return

                        self.do_trade(sell_exchange, buy_exchange, bo_list[price],
                                          so_list[_price])
                        return

    def count_orderbook(self, sell_exchange, buy_exchange, sell_price, buy_price):
        sell_exchange = eval("self." + sell_exchange)
        buy_exchange = eval("self." + buy_exchange)

        # 拿到交易卖出最大值
        sell_price = sell_price - self.profit

        buy_orderbook = buy_exchange.orderbook(self.coinType)
        sell_orderbook = sell_exchange.orderbook(self.coinType)
        if buy_orderbook:
            buy_asks = buy_orderbook.get("asks") or []
            b_amount = 0
            for a in buy_asks:
                if a["price"] < sell_price:
                    b_amount += a["amount"]

        if sell_orderbook:
            sell_bids = sell_orderbook.get("bids") or []
            s_amount = 0
            for b in sell_bids:
                if b["price"] > buy_price:
                    s_amount += a["amount"]

        self.amount = min(b_amount, s_amount)/self.dynamic_amount
        print "更改当前单次交易量为: %s" % self.amount

    @u.async
    def do_trade(self, sell_exchange, buy_exchange, sell_price, buy_price):
        fix_buy_order, fix_sell_order = "", ""
        print '-'*12 + u'profitable spread hit ' + '-'*12
        msg = u'%s > %s  sell exchange:%s sell_price: %s buy_exchange:%s  buy_price: %s  ' % (
            sell_exchange, buy_exchange, sell_exchange, sell_price, buy_exchange, buy_price)
        print msg

        sell_exchange = eval("self." + sell_exchange)
        buy_exchange = eval("self." + buy_exchange)

        sell_order = sell_exchange.sell(self.coinType, sell_price, self.amount)
        buy_order = buy_exchange.buy(self.coinType, buy_price, self.amount)

        if sell_order["result"] == "fail":
            sell_order = sell_exchange.sell(
                self.coinType, sell_price, self.amount)
    
        if buy_order["result"] == "fail":
            buy_order = buy_exchange.buy(self.coinType, buy_price, self.amount)

        if sell_order["result"] == "fail":
            fix_sell_order = buy_exchange.sell(
                self.coinType, buy_price + self.profit, self.amount)
        if buy_order["result"] == "fail":
            fix_buy_order = sell_exchange.buy(
                self.coinType, sell_price - self.profit, self.amount)

        print "sell_order: ", sell_order
        print "buy_order: ", buy_order
        print '-'*12 + u' traded ' + '-'*12
        print '\n'

        msg += "sell_order:%s  " % (sell_order)
        msg += "buy_order:%s   " % (buy_order)
        msg += "fix_buy_order:%s  " % (fix_buy_order) if fix_buy_order else ''
        msg += "fix_sell_order:%s  " % (
            fix_sell_order) if fix_sell_order else ''
        msg += '\n'

        u.Log(self.account, self.coinType, msg)

    def init_exchange(self):
        self.huobi = huobi(account=self.account)
        self.okex = okex(account=self.account)

    def start(self):
        if self.status != "on":
            print "the status is off!"
            return
        #print self.withdraw_map
        if len(self.withdraw_map) != 0:
          print "transferring, query"
          if len(self.withdraw_map) != 1:
            print "more than 1 exchange is transferring"
            return
          else:
            ex = self.withdraw_map.keys()[0]
            wid = self.withdraw_map[ex]
            #print "line 348" + str(ex) + str(wid)
            #print str(ex) + str(wid)
            ex_ins = eval("self."+ex)
            msg = ""
            qresult = ex_ins.query_withdraw(currency=self.coin, start_id=str(wid), size=100)
            #print "line 353 " + str(qresult)
            #if qresult['result'] == "success":
              #msg = qresult['msg']
            #else:
              #print qresult 
              #return
              #for c in content:
                #qid = c['id']
                #s = c['state']
                #if str(qid) == str(wid) and s == "confirmed":
                  #print "transfer finished!"
                  #self.count_all()
                  #if (abs(self.allCoin-self.pre_allCoin)/self.allCoin < 0.01):
                    #print str(self.allCoin) + "->" + str(self.pre_allCoin)
                    #del self.withdraw_map[str(ex)]
                  #else:
                    #print "transfer error, total coin reduce from %d->%d" %(self.pre_allCoin, self.allCoin)
                  #return
              #return
            if not self.HandleMsg(ex, wid, qresult):
              return
               
            else:
              print "line 376" + ex + " query withdraw failed " + str(wid)
              return
        
        self.init_exchange()

        last_price = self.get_last_price()
        if not last_price:
            print "can't get last_price"
            self.profit = self.PROFIT
        else:
            self.profit = u.get_base_spreads(
                last_price, base=self.base_bit+self.profit_bit)

        self.main()


if __name__ == '__main__':
    mh = MainHandler("usdt_neo",account="huangxinyu")
    while True:
        mh.start()
        time.sleep(1)
