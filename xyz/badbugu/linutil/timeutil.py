# -*- coding: utf-8 -*-
# DateTime  : 2022/6/28 15:40
# Author    : Badbugu17
# File      : timeutil.py
# Software  : PyCharm
import datetime
import time


# 主要是获取当前时间日期的工具类

def get_now_datetime():
    now_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # print(time.localtime())
    return now_datetime


def get_now_date():
    now_datetime = time.strftime('%Y-%m-%d', time.localtime())
    # print(time.localtime(time.time()))
    return now_datetime


def get_now_year():
    now_year = time.strftime('%Y', time.localtime())
    return now_year


def get_now_month():
    now_month = time.strftime('%m', time.localtime())
    return now_month


def get_date_by_num( year:int, month:int, day:int):
    if month < 10:
        month = '0%d'%(month)
    else:
        month = '%d'%(month)
    if day < 10:
        day = '0%d'%(day)
    else:
        day = '%d' % (day)

    return '%d-%s-%s'%(year, month, day)


def date_diff(begin: str, end: str, style='default'):
    """两个时间差，默认返回格式：0:00:00
    :param begin : 起始时间
    :param end : 结束时间
    :return timedelta类型的数据，可使用total_seconds转换成秒
    """
    begin_date = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    diff_time = end_date - begin_date
    if style == 'default':
        result_date = diff_time
    else:
        result_date = (diff_time.total_seconds())

    return result_date


def date_add_and_sub(date: str, ymd: str, number: int):
    '''
    对日期进行加减运算
    param date   : 基数日期,如果传入None则为当前日期
    param ymd    : 操作指示符 'y' 表示 年份加减. 'm' 月. 'd' 日.
    param number : 操作数,正数表示加,负数表示减
    '''
    addend = None
    now_date = datetime.datetime.strptime(get_now_date(), '%Y-%m-%d')
    if date is None:
        date = now_date
    else:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')

    number_abs = abs(number)

    # 判断闰年
    is_run = 0
    now_year = get_now_year()
    now_year = int(now_year)
    if (now_year % 4 == 0) & (now_year % 100 != 0) & (now_year % 400 == 0):
        is_run = 1
    else:
        is_run = 0

    if ymd == 'y':
        if is_run:
            addend = datetime.timedelta(days=(366*number_abs))
        else:
            addend = datetime.timedelta(days=(365*number_abs))

    if ymd == 'm':
        now_month = get_now_month()
        if ((now_month == 1) | (now_month == 3) | (now_month == 5) | (now_month == 7) |
                (now_month == 8) | (now_month == 10) | (now_month == 12)):
            addend = datetime.timedelta(days=(31*number_abs))
        elif now_month == 2:
            if is_run:
                addend = datetime.timedelta(days=(29 * number_abs))
            else:
                addend = datetime.timedelta(days=(28 * number_abs))
        else:
            addend = datetime.timedelta(days=(30*number_abs))

    if ymd == 'd':
        addend = datetime.timedelta(days=number_abs)

    result_date = None
    if number > 0:
        result_date = addend + date
    elif number < 0 :
        result_date = date - addend

    return result_date


def change_datetime_to_str(dt):
    # return_str = datetime.datetime.strftime('%Y-%m-%d %H:%M:%S', dt)
    return_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    # return_str = time.strftime('%Y-%m-%d %H:%M:%S', dt)
    return return_str


def change_date_to_str(d):
    # return_str = datetime.datetime.strftime('%Y-%m-%d', d)
    return_str = d.strftime('%Y-%m-%d')
    # return_str = time.strftime('%Y-%m-%d', d)
    return return_str

def change_str_to_datetime(datetime_str:str):
    return datetime.datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')

def change_str_to_date(date_str:str):
    return datetime.datetime.strptime(date_str,'%Y-%m-%d')

def get_week_by_date_or_datetime(date_or_datetime:datetime.datetime):
    '''
    return  :  0-6 代表 周一到周日
    '''
    if date_or_datetime is None:
        return datetime.datetime.now().weekday()
    else:
        return date_or_datetime.weekday()
