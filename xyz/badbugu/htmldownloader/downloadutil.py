# -*- coding: utf-8 -*-
# DateTime  : 2022/6/15 11:05
# Author    : Badbugu17
# File      : downloadutil.py
# Software  : PyCharm

# 针对https的安全证书 需要使用ssl
import codecs
import ssl
import time
from urllib import request
from urllib import error
from io import BytesIO
import gzip

from xyz.badbugu.htmldownloader.htmlrs import Htmlrs


class DownloadUtil:
    ssl._create_default_https_context = ssl._create_unverified_context
    headers={
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41',
        'sec-fetch-site' : 'cross-site',
        'sec-fetch-mode' : 'no-cors',
        'sec-fetch-dest' :  'empty',
        'sec-ch-ua-platform' :  'Windows',
        'sec-ch-ua-mobile' :  '?0',
        'sec-ch-ua' :  '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
        'referer' :  'https://www.bilibili.com/',
        'origin' : 'https://www.bilibili.com',
        'content-length' : '0',
        'accept-language' : 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'accept' : 'application/json, text/plain, */*'
    }

    # param url 必须添加 http://
    def downloadhtml(self,url: str):

        # self.response = urllib.request.urlopen(url)
        # print(self.response.readline())
        # print(self.response.read().decode("utf-8"))

        # 返回结果集
        html_result_set = Htmlrs()

        # 设置开始查询时间
        begin = time.time()
        html_result_set.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(begin))

        req = request.Request(url=url, headers=self.headers)
        # req = request.Request(url=url)
        response = request.urlopen(req)
        htmldom = response.read()
        # print(htmldom)
        # htmldom = str(htmldom, 'utf-8')
        # print(htmldom)
        # bytes_html_dom = BytesIO(htmldom)
        # gzip_response = gzip.GzipFile(fileobj=bytes_html_dom)

        # 结果集填充主要数据
        html_result_set.status = response.status
        # html_result_set.data = gzip_response.read().decode('utf-8')
        html_result_set.data = htmldom.decode('utf-8')
        print(html_result_set.data)

        # 设置开始查询时间
        end = time.time()
        html_result_set.endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(end))
        html_result_set.diff = round((end - begin), 2)

        return html_result_set



