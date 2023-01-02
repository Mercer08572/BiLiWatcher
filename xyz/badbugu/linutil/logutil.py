# -*- coding: utf-8 -*-
# DateTime  : 2022/8/6 10:07
# Author    : Badbugu17
# File      : logutil.py
# Software  : PyCharm
import logging
import os.path

from xyz.badbugu.linutil import timeutil

current_path = os.path.dirname(__file__)
log_path = os.path.join(current_path, '../logs')


class LogUtil:
    def __init__(self, log_path=log_path):
        self.logfile_path = log_path
        # 创建日志对象logger
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            # 设置日志级别
            self.logger.setLevel(logging.INFO)
            # 日志格式
            formatter = logging.Formatter('%(asctime)s-[%(filename)s-->line:%(lineno)d]-%(levelname)s:%(message)s')

            # 在文件中输出日志
            # 一天一个日志文件
            self.log_name_path = os.path.join(self.logfile_path, 'BLW_%s.log' % timeutil.get_now_date() )
            # 创建文件处理程序并实现追加
            self.file_log = logging.FileHandler(self.log_name_path, 'a', encoding='utf-8')
            # 设置日志文件的格式
            self.file_log.setFormatter(formatter)
            # 设置日志级别
            self.file_log.setLevel(logging.INFO)
            # 把日志信息输出到文件中
            self.logger.handlers = []
            self.logger.addHandler(self.file_log)
            # 关闭文件
            self.file_log.close()

            # 在控制台输出日志
            # 日志在控制台输出
            self.console = logging.StreamHandler()
            # 设置日志级别
            self.console.setLevel(logging.INFO)
            # 设置日志格式
            self.console.setFormatter(formatter)
            # 把日志信息输出到控制台\
            self.logger.removeHandler(self.console)
            self.logger.addHandler(self.console)
            self.logger.removeHandler(self.console)
            # 关闭控制台日志
            self.console.close()

    def get_log(self):
        return self.logger


# logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s-[%(filename)s-->line:%(lineno)d]-%(levelname)s:%(message)s')
#
# def log_warning(msg:str):
#     logging.warning(msg)
#
# def log_debug(msg:str):
#     logging.debug(msg)
#
# def log_info(msg: str):
#     logging.info(msg)
#
# def log_error(msg: str):
#     logging.error(msg)
#
# def log_critical(msg:str):
#     logging.critical(msg)