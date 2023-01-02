# -*- coding: utf-8 -*-
# DateTime  : 2022/6/15 10:33
# Author    : Badbugu17
# File      : dmlutil.py
# Software  : PyCharm
import time

import pymysql
from pymysql import cursors

from xyz.badbugu.dbtool.connutil import ConnUtil
from xyz.badbugu.dbtool.resultset import ResultSet
from xyz.badbugu.linutil.logutil import LogUtil


class DmlUtil:

    logutil = LogUtil()
    logger = logutil.get_log()

    # 查询sql语句执行结果封装方法 返回resultSet类型的数据
    def __execute_sql(self, cursor: cursors, sql: str):
        #
        resultSet = ResultSet()
        resultSet.type = 1.1
        # 设置开始查询时间
        begin = time.time()
        resultSet.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(begin))
        cursor.execute(sql)
        # 设置查询结束时间
        end = time.time()
        resultSet.endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end))
        resultSet.diff = round((end - begin), 2)
        resultSet.data = cursor.fetchall()
        self.logger.info("执行sql:%s.执行时间:%dms" % (sql, resultSet.diff))

        return resultSet

    # 非查询类语句执行结果封装
    def __execute_do_sql(self, cursor: cursors, sql: str):
        resultSet = ResultSet()
        resultSet.type = 1.2
        # 设置开始查询时间
        begin = time.time()
        resultSet.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(begin))
        cursor.execute(sql)
        # 设置查询结束时间
        end = time.time()
        resultSet.endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end))
        resultSet.diff = round((end - begin), 2)
        resultSet.data = 'OK'
        self.logger.info("执行sql:%s.执行时间:%dms" % (sql, resultSet.diff))

        return resultSet

    # 非查询类语句批量处理
    def __execute_batch_do_sql(self, cursor: cursors, sqlList: list):

        resultSet = ResultSet()
        resultSet.type = 1.2
        # 设置开始执行时间
        begin = time.time()
        resultSet.beginTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(begin))
        for sql in sqlList:
            cursor.execute(sql)

        # 设置查询结束时间
        end = time.time()
        resultSet.endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end))
        resultSet.diff = round((end - begin), 2)
        resultSet.data = 'OK'
        self.logger.info("批量执行sql.执行时间:%dms" % resultSet.diff)

        return resultSet


    # # 获取最大主键
    # def getMaxPrimaryKeyValue(self,tablename: str):
    #     cursor = ConnUtil._getConnector()

    # 执行查询sql语句
    def query_sql(self, sql: str):

        # 实例化数据库连接类
        connUtil = ConnUtil()
        connector = None
        cursor = None

        try:

            connector = connUtil.get_connector()  # 获取数据库连接
            cursor = connUtil.get_cursor(connector)  # 获取数据库指针

            resultSet = self.__execute_sql(cursor, sql)
        except Exception as e:
            print(e)
            self.logger.error("执行slq:%s时出现问题：%s" % (sql, e))
            raise e
        else:
            return resultSet

        finally:
            connUtil.close_cursor(cursor)
            connUtil.close_connector(connector)

    # 执行非查询单条sql语句
    def do_sql(self, sql: str):

        # 实例化数据库连接类
        connUtil = ConnUtil()
        connector = None
        cursor = None

        try:
            connector = connUtil.get_connector()  # 获取数据库连接
            cursor = connUtil.get_cursor(connector)  # 获取数据库指针

            resultSet = self.__execute_do_sql(cursor, sql)

        except Exception as e:
            print(e)
            self.logger.error("执行slq:%s时出现问题：%s" % (sql, e))
            raise e
        else:
            return resultSet

        finally:
            connUtil.close_cursor(cursor)
            connUtil.close_connector(connector)

    # 批量执行非查询类sql语句
    def batch_do_sql(self, sqlList: list):

        # 实例化数据库连接类
        connUtil = ConnUtil()
        connector = None
        cursor = None

        try:
            connector = connUtil.get_connector()  # 获取数据库连接
            cursor = connUtil.get_cursor(connector)  # 获取数据库指针

            resultSet = self.__execute_batch_do_sql(cursor, sqlList)

        except Exception as e:
            print(e)
            self.logger.error("批量执行slq时出现问题：%s" % e)
            raise e

        else:
            return resultSet

        finally:
            connUtil.close_cursor(cursor)
            connUtil.close_connector(connector)