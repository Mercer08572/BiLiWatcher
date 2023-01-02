# -*- coding: utf-8 -*-
# DateTime  : 2022/8/26 17:05
# Author    : Badbugu17
# File      : Test001.py
# Software  : PyCharm
from xyz.badbugu.dbtool.dmlutil import DmlUtil
from xyz.badbugu.linutil import timeutil
from xyz.badbugu.pureinterface.biliapi import Biliapi

# rs = DmlUtil().query_sql('select list.mid, list.name, list.sex, list.level, list.video_number, list.begin_watch_date, trend.watch_times from blw_watchlist as list, blw_upfanstrend as trend where list.mid = trend.mid')
# print(type(rs.data[0][5]))
#
#
# print(timeutil.change_datetime_to_str(rs.data[0][5]))
b = Biliapi()
print('获取视频数')
print(b.get_up_video_number(14110780))
print('获取粉丝数')
print(b.get_up_fans(14110780))
print('获取up信息')
print(b.get_up_info(14110780))
