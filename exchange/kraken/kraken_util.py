#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hmac
import hashlib
import json

import urllib
import datetime
import requests
import urllib2
import urlparse
import connection
import time
from util.util import *

# timeout in 5 seconds:
TIMEOUT = 5

API_HOST = "https://api.kraken.com"

SCHEME = "https"


API_KEY = ""

API_SECRET = ""

DEFAULT_GET_HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': 'en',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

DEFAULT_POST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': 'en',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

def _query(urlpath, req = {}, conn = None, headers = {}):
        """Low-level query handling.
        
        Arguments:
        urlpath -- API URL path sans host (string, no default)
        req     -- additional API request parameters (default: {})
        conn    -- kraken.Connection object (default: None)
        headers -- HTTPS headers (default: {})
        
        """
        url = API_HOST + urlpath

        if conn is None:
            conn = connection.Connection()

        ret = conn._request(url, req, headers)
        print "111",ret
        return json.loads(ret)


def query_public(method, req = {}, conn = None):
    """API queries that do not require a valid key/secret pair.
    
    Arguments:
    method -- API method name (string, no default)
    req    -- additional API request parameters (default: {})
    conn   -- connection object to reuse (default: None)
    
    """
    urlpath = '/0/public/' + method

    return _query(urlpath, req, conn)

    
def query_private(method, req={}, conn = None, account= None):
    """API queries that require a valid key/secret pair.
    
    Arguments:
    method -- API method name (string, no default)
    req    -- additional API request parameters (default: {})
    conn   -- connection object to reuse (default: None)
    
    """
    urlpath = '/0/private/' + method

    req['nonce'] = int(1000*time.time())
    req["otp"] = "584hxy.."
    postdata = urllib.urlencode(req)
    print postdata
    # API_KEY, API_SECRET = get_account_key("kraken", account)
    API_KEY, API_SECRET = "WhoH8CMwnUB1PmL9sYN4ibw1pk3JIHC1FuVLZnhLjz1f+yJXVaJNWY0E","cgA1h6KYlsDcRD/u0+KXRZ7fdRoONX1lNmju/lyl82cdCO1Rvt/pgMzx8IrdHrpO+y/mCdc/Y6/rmCsV2y9fqg=="
    message = urlpath + hashlib.sha256(str(req['nonce']) +
                                       postdata).digest()
    signature = hmac.new(base64.b64decode(API_SECRET),
                         message, hashlib.sha512)
    headers = {
        'API-Key': API_KEY,
        'API-Sign': base64.b64encode(signature.digest())
    }

    return _query(urlpath, req, conn, headers)
