# -*- coding: utf-8 -*-
# DateTime  : 2022/6/17 19:19
# Author    : Badbugu17
# File      : biliapi.py
# Software  : PyCharm
# from urllib import request
import requests

from xyz.badbugu.linutil.logutil import LogUtil


class Biliapi:

    logutil = LogUtil()
    logger = logutil.get_log()

    # https://api.bilibili.com/x/relation/stat?vmid=562197&jsonp=jsonp
    # https://api.bilibili.com/x/relation/stat?vmid=559186307&jsonp=jsonp
    # 获取up粉丝数
    GET_UP_FANS_URL = 'https://api.bilibili.com/x/relation/stat'

    # https://api.bilibili.com/x/space/acc/info?mid=63004746&jsonp=jsonp
    # 获取up个人信息
    GET_UP_INFO_URL = 'https://api.bilibili.com/x/space/acc/info'

    # https://api.bilibili.com/x/space/arc/search?mid=562197&pn=1&ps=25&index=1&jsonp=jsonp  过期API
    # https://api.bilibili.com/x/space/wbi/arc/search?mid=559186307&ps=30&tid=0&pn=1&keyword=&order=pubdate&order_avoided=true 获取up主视频数也可以使用这个aip
    # 获取up主视频数
    GET_UP_VIDEO_NUMBER_URL = 'https://api.bilibili.com/x/space/wbi/arc/search'

    # https://api.bilibili.com/x/space/arc/search?mid=562197&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp
    # https://api.bilibili.com/x/space/wbi/arc/search?mid=559186307&ps=30&tid=0&pn=1&keyword=&order=pubdate&order_avoided=true
    #获取up主channel
    GET_UP_CHANNEL_URL = 'https://api.bilibili.com/x/space/arc/search'

    # 请求头
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
        # 'referer': 'https://space.bilibili.com/63004746?spm_id_from=333.337.0.0',
        'origin': 'https://space.bilibili.com',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept': 'application/json, text/plain, */*',
        # ':scheme': 'https',
        # ':path': '/x/relation/stat?vmid=63004746&jsonp=jsonp',
        # ':method': 'GET',
        # ':authority': 'api.bilibili.com'
    }

    # 获取用户的粉丝数
    def get_up_fans(self, uid: int):
        # payload = {
        #     'vmid' : uid,
        #     'jsonp' : 'jsonp'
        # }
        payload = {}

        url = '%s?vmid=%d&jsonp=jsonp' % (self.GET_UP_FANS_URL, uid)
        # print('%s?vmid=%d&jsonp=jsonp'%(self.GAT_UP_FANS_URL, uid))
        # response = request.Request("GET", self.GAT_UP_FANS_URL, headers=headers, data=payload)
        self.logger.info('调用B站API_get_up_fans,请求地址为：%s' % url)
        response = requests.request("GET", url, headers=self.HEADERS, data=payload)

        # print(response.text)

        re_response_text = response.text
        # self.logger.info("调用B站API，返回报文为：%s" % re_response_text)

        # print(type(re_response_text))
        # re_response_text = re_response_text.encode('GBK')
        # re_response_text = re_response_text.decode('utf-8')

        return re_response_text

    def get_up_info(self, uid: int):
        payload = {}

        url = '%s?mid=%d&jsonp=jsonp' % (self.GET_UP_INFO_URL, uid)
        # print(url)
        self.logger.info('调用B站API_get_up_info,请求地址为：%s' % url)
        response = requests.request("GET", url, headers=self.HEADERS, data=payload)

        re_response_text = response.text
        # self.logger.info("调用B站API，返回报文为：%s" % re_response_text)

        # print(re_response_text)
        # re_response_text = re_response_text.encode('gbk').decode('utf-8')

        return re_response_text

    def get_up_video_number(self, uid: int):
        payload = {}

        url = '%s?mid=%d&ps=30&tid=0&pn=1&keyword=&order=pubdate&order_avoided=true' % (self.GET_UP_VIDEO_NUMBER_URL, uid)
        # url = '%s?mid=%d' % (self.GET_UP_VIDEO_NUMBER_URL, uid)
        self.logger.info('调用B站API_get_up_video_number,请求地址为：%s' % url)
        response = requests.request("GET", url, headers=self.HEADERS, data=payload)

        re_response_text = response.text
        # self.logger.info("调用B站API，返回报文为：%s" % re_response_text)

        return re_response_text

    def get_up_channel(self, uid: int):
        payload = {}

        url = '%s?mid=%d&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp' % (self.GET_UP_CHANNEL_URL, uid)
        self.logger.info('调用B站API_get_up_channel,请求地址为：%s' % url)
        response = requests.request("GET", url, headers=self.HEADERS, data=payload)

        re_response_text = response.text
        # self.logger.info("调用B站API，返回报文为：%s" % re_response_text)

        return re_response_text
