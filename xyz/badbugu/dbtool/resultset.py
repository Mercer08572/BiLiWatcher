# -*- coding: utf-8 -*-
# DateTime  : 2022/6/15 10:32
# Author    : Badbugu17
# File      : resultset.py
# Software  : PyCharm
class ResultSet:
    beginTime = ""
    type = 1.1  # 1：DML 1.1: 查 1.2: 增 删 改  2 DDL
    data = None
    endTime = ""
    diff = None

    def to_string(self):
        print(self.beginTime)
        print(self.endTime)
        print(self.diff)
        print(self.type)
        print(self.data)