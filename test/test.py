import sys 
import time
sys.path.append("../../crossexchangearb")
from exchange import *

def DoTransfer(source, dest, dest_address):
  pass

'''
hb = huobi(account = "huangxinyu")
#wre = hb.withdraw(currency="xrp", address="rUzWJkXyEtT8ekSSxkBYPqCvHpngcy6Fks", amount="30", addr_tag="90678")
time.sleep(3)
#print wre
wid=''
raw_re = hb.query_withdraw(currency="xrp", id=wid, size=10)
re = raw_re['msg']
for a in re:
    print str(a['id']) + ": " + a['state']
#print raw_re
'''
'''
if wre['result']=='success':
  wid = wre['msg']
  print 'id is ' + str(wid)
  raw_re = hb.query_withdraw(currency="xrp", id=wid, size=10)
  print raw_re
  re = raw_re['msg']
  for a in re:
    print str(a['id']) + ": " + a['state']
'''
#print(ox.funds_transfer(coinType="xrp_usd", amount=30, From="1", To="6"))
ox = okex(account="huangxinyu")
re = ox.withdraw(currency = "xrp", address = "r4t2K7yKHvQ1RmznNssRRv6QMTBw8uDZQ7", amount = "20.0", fee = "0.15", addr_tag="107250")
#print(ox.withdraw(currency = "neo", address = "AXytguxobRqWptKvtTufs5dWtf6dW6St7b", amount = "1.0", fee = "0.0", addr_tag="address"))
#re = ox.query_withdraw(currency='xrp_usd', start_id = "1799648", size =100)
#print type(result)
#print result
#re = ox.getWalletInfo()
#re = ox.funds_transfer("xrp", amount='10', From='1', To='6')
print re
