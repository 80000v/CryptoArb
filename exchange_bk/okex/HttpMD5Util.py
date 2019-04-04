#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于进行http请求，以及MD5加密，生成签名的工具类

import requests
import hashlib

#初始化apikey，secretkey,url
apikey = '1cd704d7-d549-436b-a5ee-df7e401843d3'
secretkey = '1AE1EE7238F5485D35E128194B821181'
okcoinRESTURL = 'https://www.okcoin.cn'
BaseUrl = "/v2/auth/login"

DEFAULT_POST_HEADERS = {
# "Authorization":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI5NjQ5MGI4Ni0zOWExLTQyMWEtYmEzYi03YTAxNTkwYTg1N2MiLCJhdWRpZW5jZSI6IndlYiIsImNyZWF0ZWQiOjE1MDE1NTkzMzE0MzEsImV4cCI6MTUwMjE2NDEzMX0.crVupk8Tc4ki_TIT-tLmTpBxEjdOt4Ww3b3GoP0TJebCUT_TIxvBjzeTFRnnchbGwUHvrSoqp0cVofVaENkA6Q"
"Authorization":None,
'Content-Type': 'application/json',
"User-Agent": "Chrome/39.0.2171.71",
"Accept": "application/json",
"authRequest":"authRequest"
}


def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    data = sign+'secret_key='+secretKey
    return  hashlib.md5(data.encode("utf8")).hexdigest().upper()

def httpGet(url,resource,params=''):
    # conn = http.client.HTTPSConnection(url, timeout=10)
    # conn.request("GET",resource + '?' + params)
    # response = conn.getresponse()
    # data = response.read().decode('utf-8')
    # return json.loads(data)
    try:
        response = requests.get(url, params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"result":"fail"}
    except Exception as e:
        print("httpGet failed, detail is:%s" % e)
        return

def httpPost(url,resource,params):
     headers = {
            "Content-type" : "application/x-www-form-urlencoded",
     }
     # conn = http.client.HTTPSConnection(url, timeout=10)
     # temp_params = urllib.parse.urlencode(params)
     # conn.request("POST", resource, temp_params, headers)
     # response = conn.getresponse()
     # data = response.read().decode('utf-8')
     # params.clear()
     # conn.close()
     # return data
     try:
        if resource:
            url = url + resource
        response = requests.post(url, params, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return
     except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return "fail"


        
     
