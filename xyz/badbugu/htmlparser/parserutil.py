# -*- coding: utf-8 -*-
# DateTime  : 2022/6/15 15:32
# Author    : Badbugu17
# File      : parserutil.py
# Software  : PyCharm
from bs4 import BeautifulSoup

from xyz.badbugu.htmldownloader.htmlrs import Htmlrs
# 使用beautifulsoup4 进行网页解析
class Parserutil:

    # 两个方法，方法一，解析博主粉丝数。 方法二，拼装为sql语句
    #

    def get_up_fans(self, htmlrs: Htmlrs):
        htmldom = htmlrs.data;
        #转换成beautifulsoup对象
        htmlbs = BeautifulSoup(htmldom)

