#!/usr/bin/env python3
"""
CiNii ArticleのAPIをCSVに
"""

import urllib3
import urllib.parse
import certifi
import pandas as pd
import csv
import sys
import json
import time

#APPID = "xxxxx" # APPIDはCiNiiで取得してセット
APPID = "CiNii09-89ef94917d5946d2a0dae832519f760b"
keyword2 = "オープンサイエンス"
keyword = urllib.parse.quote(keyword2)
count = 50

req_url = 'https://ci.nii.ac.jp/opensearch/search?format=json'
req_url = req_url + "&appid=" + APPID
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

def req(keyword, start):
   req_url2 = req_url + "&q=" + keyword + "&start=" + str(start) + "&count=" + str(count)
   print(req_url2)
   response = http.request('GET', req_url2)
   json_data = response.data.decode('utf-8')
   time.sleep(0.5)
   return json_data

data_dict1 = json.loads(req(keyword,1))
totalResults = data_dict1["@graph"][0]["opensearch:totalResults"] # 総件数
print("totalResults: ",totalResults)

data_dict = pd.DataFrame()

num = 1
while True:
    json_data2 = req(keyword,num)
    try:
        data_dict = data_dict.append( pd.read_json(json.dumps(json.loads(json_data2)["@graph"][0]["items"])) ,sort="true")
    except Exception:
        pass
    # 
    num = num + count
    if num > int(totalResults) :
        break

# CSV出力
data_dict.to_csv('ciniia_data.csv', encoding='utf-8_sig', quoting=csv.QUOTE_ALL, index=False )