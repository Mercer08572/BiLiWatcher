# -*- coding: utf-8 -*-
# DateTime  : 2022/6/15 10:27
# Author    : Badbugu17
# File      : connutil.py
# Software  : PyCharm
import pymysql

# 进行数据库连接
# getConnect() 获取cursor，建立数据库连接。
# closeConnetc(cursor)，关闭数据库连接。
from pymysql import cursors


class ConnUtil:

    # 获取数据库信息，创建连接并返回dbconn，目前是直接获取的样式，之后会改成从配置文件中获取
    def get_connector(self):

        try:
            dbconn = pymysql.connect(
                host='',
                port=,
                user='',
                password='',
                database='',
                charset='gbk'
            )
        except Exception as e:
            print(e)
            raise e
        else:
            return dbconn

    # 获取指针
    def get_cursor(self, dbconn: pymysql.connections.Connection):
        cursor = dbconn.cursor()
        # cursor.execute()
        return cursor

    # 关闭数据库指针
    def close_cursor(self, cursor: cursors):
        cursor.close()

    # 关闭数据库连接，在进行数据库操作之后，必须关闭数据库连接
    def close_connector(self, dbconn: pymysql.connections.Connection):
        dbconn.close()