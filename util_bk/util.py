import functools
import threading
import time
from datetime import datetime
from ConfigParser import ConfigParser



def get_base_spreads(price, base= 0.001):
    price = float(price)
    return abs(price * base)


def get_account_key(exchange, account=None):
    if not account:
        return None, None
    cf = ConfigParser()
    cf.read('/home/zentero/crossexchangearb/config/%s.ini' % account)
    apikey = cf.get('%s' % exchange, 'api_key')
    secretkey = cf.get('%s' % exchange, 'secret_key')
    return apikey, secretkey

def async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        my_thread.setDaemon(True)
        my_thread.start()
    return wrapper

@async
def Log(owner, coinType, msg):
    now_md = time.strftime("%Y%m%d")
    with open('log/%s_%s_%s.log' % (owner,coinType, now_md), 'a') as t:
        now = datetime.now()
        str_time = now.strftime('%Y-%m-%d %H:%M:%S')
        msg = "[" + str_time + "]" + ' ' + msg
        t.write(msg)

@async
def dblog(coinType, msg):
    pass

@async
def alert(coinType, msg):
    pass

@async
def wxbot(coinType, msg):
    pass
