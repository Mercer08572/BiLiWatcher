# -*- coding: utf-8 -*-
# DateTime  : 2022/6/20 14:40
# Author    : Badbugu17
# File      : bilischeduler.py
# Software  : PyCharm
import json
import math

from xyz.badbugu.dbtool.dmlutil import DmlUtil
from xyz.badbugu.linutil import timeutil
from xyz.badbugu.linutil.logutil import LogUtil
from xyz.badbugu.pureinterface.biliapi import Biliapi


class BiliScheduler:
    logutil = LogUtil()
    logger = logutil.get_log()

    dmlutil = DmlUtil()
    biliapi = Biliapi()

    def begin_get_info(self):
        self.logger.info("############################本次处理开始############################")
        print("############################本次处理开始############################")
        loop_begin_time = ''
        loop_end_time = ''
        loop_10_begin = ''
        loop_10_end = ''

        # step1 读取数据表 每次读取10条数据

        # step1.1 查询数据表watchlist总记录数 计算循环几次
        countSql = 'select count(watch_id) from blw_watchlist'
        rs = self.dmlutil.query_sql(countSql)
        watch_number = rs.data[0][0]
        # 除于10求商 判断循环几次
        loop_count = math.ceil(watch_number / 10)  # 向上取整

        # 10位up主一起更新的起始位置
        loop_begin_time = timeutil.get_now_datetime()
        # self.logger.info('****************************10位up主一组，进行数据处理开始时间为:%s'
        #                  '****************************' % loop_begin_time)
        for i in range(loop_count):
            '''记录日志'''
            loop_10_begin = timeutil.get_now_datetime()
            self.logger.info('$$$$$$$$$$$$$$$$$$$$$$$$$$$$第%d次10循开始时间：%s'
                             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$' % ((i + 1), loop_10_begin))
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$第%d次10循开始时间：%s'
                  '$$$$$$$$$$$$$$$$$$$$$$$$$$$$' % ((i + 1), loop_10_begin))
            # 第一次获取前10位数, 第二次获取11到20
            query_sql = 'select * from blw_watchlist ORDER BY watch_id ASC LIMIT %d,10' % (i * 10)
            # print(query_sql)
            # 执行sql语句，获取用户uid
            result_set = self.dmlutil.query_sql(query_sql)
            each_watch_count = (len(result_set.data))

            # step2 获取用户信息，更新 watchlist表
            # update_sql.clear()
            # insert_sql_record.clear()

            '''记录日志'''
            watch_begin_time = timeutil.get_now_datetime()
            self.logger.info('****************************三表处理开始：%s'
                             '****************************' % watch_begin_time)
            print('****************************三表处理开始：%s'
                  '****************************' % watch_begin_time)

            for j in range(each_watch_count):
                uid_from_database = result_set.data[j][1]

                '''查询是否有watch_date为今天的记录存在于blw_upfansrecord表中,如果有，flag2直接设置为OK，不再进行数据插入'''
                '''进行插入判断，减少数据库操作次数，节约资源'''
                '''更新判断，减少数据库操作次数，节约资源'''
                check_today_exist_sql = "select count(mid) from blw_upfansrecord where mid = %d and watch_date = '%s'" \
                                        % (uid_from_database, timeutil.get_now_date())
                check_rs = self.dmlutil.query_sql(check_today_exist_sql)
                check_rs_flag = check_rs.data[0][0]

                '''记录日志'''
                watchlist_deal_begin_time = timeutil.get_now_datetime()
                self.logger.info('****************************list表处理开始：%s'
                                 '****************************' % watchlist_deal_begin_time)

                try:

                    if check_rs_flag == 0:

                        # 应该有一个异常处理

                        # 调用接口获取up主信息 主要信息包括，name, sex, level, official_title, birthday, school
                        response_text = self.biliapi.get_up_info(uid_from_database)

                        json_response_text = json.loads(response_text)
                        # print(type(json_response_text))
                        data = json_response_text.get('data')
                        # print(type(data))
                        # data = json.loads(data)
                        name = data.get('name')
                        name = name.replace(u'\xd8', u'')

                        sex = data.get('sex')
                        if sex == '男':
                            sex = 1
                        elif sex == '女':
                            sex = 0
                        else:
                            sex = 3  # 未知

                        level = data.get('level')

                        official_title = data.get('official').get('title')
                        official_title = official_title.replace(u'\xa0', u'')

                        birthday = data.get('birthday')

                        school = data.get('school')
                        if school is not None:
                            school = school.get("name")
                        else:
                            school = None

                        # 获取up主粉丝数
                        response_vn = self.biliapi.get_up_video_number(uid_from_database)
                        # print(vn)
                        json_vn = json.loads(response_vn)
                        vn = (json_vn.get('data').get('page').get('count'))

                        # 预测up主频道
                        tid_count_list, max_tid = self.forecast_up_channel(json_vn)

                        # 拼装成update语句存入 update_sql 中
                        # 观察日期
                        each_update_sql = "update blw_watchlist set name = '%s', sex = %d, birthday = '%s', school = '%s', " \
                                          "level = %d, title = '%s', video_number = %d, " \
                                          "channels = '%s', channel = %d, " \
                                          "begin_watch_date = '%s' " \
                                          "where mid = %s" % (name, sex, birthday, school, level, official_title,
                                                              vn, tid_count_list, max_tid,
                                                              timeutil.get_now_datetime(), uid_from_database)
                        # update_sql.append(each_update_sql)
                        watchlist_update_rs = self.dmlutil.do_sql(each_update_sql)
                        '''flag1'''
                        flag1 = watchlist_update_rs.data  # flag1 是blw_watchlist表是否插入成功的标识

                    else:
                        flag1 = 'OK'

                except Exception as e:
                    self.logger.error("出现异常：" + str(e))
                    flag1 = 'OFF'

                # 此处try结束

                '''记录日志'''
                watchlist_deal_end_time = timeutil.get_now_datetime()
                self.logger.info('****************************list表处理耗时：%s'
                                 '****************************' % timeutil.date_diff(watchlist_deal_begin_time,
                                                                                     watchlist_deal_end_time))
                print('****************************list表处理耗时：%s'
                      '****************************' % timeutil.date_diff(watchlist_deal_begin_time,
                                                                          watchlist_deal_end_time))

                try:

                    # step3 获取用户的粉丝信息 添加信息到 upfansrecord, 更新upfanstrend表
                    '''粉丝数记录表'''
                    # 拼装record insert语句
                    # insert into blw_upfansrecord(mid, fans_number, watch_date) values()
                    response_fans = self.biliapi.get_up_fans(uid_from_database)
                    json_fans = json.loads(response_fans)
                    fans = (json_fans.get('data').get('follower'))

                    flag2 = ''

                    '''记录日志'''
                    record_deal_begin_time = timeutil.get_now_datetime()
                    self.logger.info('****************************record表处理开始：%s'
                                     '****************************' % record_deal_begin_time)

                    if check_rs_flag == 0:  # 说明upfansrecord表中没有今日该mid的记录，则进行插入数据
                        each_insert_record_sql = "insert into blw_upfansrecord(mid, fans_number, watch_date) " \
                                                 "values(%d, %d, '%s')" % (uid_from_database, fans, timeutil.get_now_date())
                        # insert_sql_record.append(each_insert_record_sql)
                        upfansrecord_insert_rs = self.dmlutil.do_sql(each_insert_record_sql)
                        '''flag2'''
                        flag2 = upfansrecord_insert_rs.data  # flag2 是blw_upfansrecord表是否插入成功的标识
                        # print(each_update_sql)
                    else:
                        flag2 = 'OK'

                except Exception as e:
                    self.logger.error("出现异常：" + str(e))
                    flag2 = 'OFF'

                '''记录日志'''
                record_deal_end_time = timeutil.get_now_datetime()
                self.logger.info('****************************record表处理耗时：%s'
                                 '****************************' % timeutil.date_diff(record_deal_begin_time,
                                                                                     record_deal_end_time))
                print('****************************record表处理耗时：%s'
                      '****************************' % timeutil.date_diff(record_deal_begin_time,
                                                                          record_deal_end_time))

                try:

                    '''记录日志：trend表处理耗时'''
                    trend_deal_begin_time = timeutil.get_now_datetime()
                    self.logger.info('****************************trend表处理开始：%s'
                                     '****************************' % trend_deal_begin_time)

                    '''只有flag1 和 flag2 同时为 ok时，才可进行粉丝趋势表的操作 '''
                    if (flag1 == 'OK') & (flag2 == 'OK'):

                        '''粉丝趋势表,watch_times，fans_now, 
                        fans_one一天前的粉丝数, fans_three 三天前的粉丝数, seven七天， fifteen十五天, 
                        fans_one_m,一个月前, three_m 三个月, six_m 六个月, fans_one_y 一年， fans_compare_begin 和最早一次粉丝数比较
                        fans_rate1,2,3,4,5,6,7,8,9'''
                        # 现在blw_upfanstrend表中查找up主的mid看是否有记录，若无记录，则添加新纪录，如果有记录则更新
                        trend_find_sql = 'select count(tid) from blw_upfanstrend where mid = %d' % uid_from_database
                        trend_resultSet = self.dmlutil.query_sql(trend_find_sql)
                        if_exist_trend_flag = trend_resultSet.data[0][0]
                        if if_exist_trend_flag == 1:  # 有记录，更新strend表中的数据

                            # last_update按今天的日期查询trend表，如果没查到，说明本日没有处理trend表，则进行更新
                            is_today_update_trend_sql = "select count(tid) from blw_upfanstrend " \
                                                        "where mid = %d and last_update = '%s'" \
                                                        % (uid_from_database, timeutil.get_now_date())
                            today_update_trend_rs = self.dmlutil.query_sql(is_today_update_trend_sql)

                            if today_update_trend_rs.data[0][0] != 1:  # trend表中没有今日数据，进行更新

                                # 说明trend表中有记录，只需要更新数据即可。 step1 在record表中查找最近的一次日期，然后计算trend
                                # 计算 watch_time
                                watch_time_sql = 'select count(rid) from blw_upfansrecord where mid = %d' % uid_from_database
                                wts_rs = self.dmlutil.query_sql(watch_time_sql)
                                watch_times = wts_rs.data[0][0]

                                # 计算fans_one setp1 查找前一天的record
                                fand_fans_rate_sql_list = []
                                fans_before_list = []
                                fans_rate_list = []
                                # 一天前
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord "
                                                               "where watch_date = '%s' and mid = %d"
                                                               % (timeutil.date_add_and_sub(timeutil.get_now_date(),
                                                                                            'd', 'sub', 1),
                                                                  uid_from_database))
                                # 三天前
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord "
                                                               "where watch_date = '%s' and mid = %d"
                                                               % (timeutil.date_add_and_sub(timeutil.get_now_date(),
                                                                                            'd', 'sub', 3),
                                                                  uid_from_database))
                                # 七天前
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord "
                                                               "where watch_date = '%s' and mid = %d"
                                                               % (timeutil.date_add_and_sub(timeutil.get_now_date(),
                                                                                            'd', 'sub', 7),
                                                                  uid_from_database))
                                # 十五天前
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord "
                                                               "where watch_date = '%s' and mid = %d"
                                                               % (timeutil.date_add_and_sub(timeutil.get_now_date(),
                                                                                            'd', 'sub', 15),
                                                                  uid_from_database))
                                # 一个月前
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord "
                                                               "where watch_date = '%s' and mid = %d"
                                                               % (timeutil.date_add_and_sub(timeutil.get_now_date(),
                                                                                            'm', 'sub', 1),
                                                                  uid_from_database))
                                # 三个月前
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord "
                                                               "where watch_date = '%s' and mid = %d"
                                                               % (timeutil.date_add_and_sub(timeutil.get_now_date(),
                                                                                            'm', 'sub', 3),
                                                                  uid_from_database))
                                # 六个月前
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord "
                                                               "where watch_date = '%s' and mid = %d"
                                                               % (timeutil.date_add_and_sub(timeutil.get_now_date(),
                                                                                            'm', 'sub', 6),
                                                                  uid_from_database))
                                # 一年前
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord "
                                                               "where watch_date = '%s' and mid = %d"
                                                               % (timeutil.date_add_and_sub(timeutil.get_now_date(),
                                                                                            'y', 'sub', 1),
                                                                  uid_from_database))
                                # 本次fans和第一次fans对比
                                fand_fans_rate_sql_list.append("select fans_number from blw_upfansrecord where "
                                                               "watch_date = (select min(watch_date) "
                                                               "from blw_upfansrecord where mid = %d) and mid = %d "
                                                               % (uid_from_database, uid_from_database))
                                for k in range(len(fand_fans_rate_sql_list)):
                                    fand_fans_rs = self.dmlutil.query_sql(fand_fans_rate_sql_list[k])
                                    is_none = len(fand_fans_rs.data)
                                    if is_none:  # 不为空
                                        # 说明record表中有需要的数据，进行数据处理
                                        target_fans = fand_fans_rs.data[0][0]
                                        fans_before_list.append(target_fans)  # 获取查询列表的第一条数据的第一个元素
                                        # 计算rate 增长率 = (今天fans-目标fans)/目标fans
                                        fans_rate_list.append(((fans - target_fans) / target_fans) * 100)
                                    else:
                                        fans_before_list.append(0)
                                        fans_rate_list.append(0)

                                each_update_sql_strend = "update blw_upfanstrend set watch_times = %d, fans_now = %d, " \
                                                         "fans_one = %d, fans_three = %d, fans_seven = %d, fans_fifteen = %d," \
                                                         "fans_one_m = %d, fans_three_m = %d, fans_six_m = %d, " \
                                                         "fans_one_y = %d, " \
                                                         "fans_compare_begin = %d, fans_rate1 = %.2f, fans_rate2 = %.2f, " \
                                                         "fans_rate3 = %.2f, fans_rate4 = %.2f, fans_rate5 = %.2f, " \
                                                         "fans_rate6 = %.2f," \
                                                         "fans_rate7 = %.2f, " \
                                                         "fans_rate8 = %.2f, " \
                                                         "fans_rate9 = %.2f, " \
                                                         "last_update = '%s' " \
                                                         "where mid = %s" \
                                                         % (watch_times, fans, fans_before_list[0], fans_before_list[1],
                                                            fans_before_list[2], fans_before_list[3], fans_before_list[4],
                                                            fans_before_list[5], fans_before_list[6], fans_before_list[7],
                                                            fans_before_list[8], fans_rate_list[0], fans_rate_list[1],
                                                            fans_rate_list[2], fans_rate_list[3], fans_rate_list[4],
                                                            fans_rate_list[5], fans_rate_list[6], fans_rate_list[7],
                                                            fans_rate_list[8], timeutil.get_now_date(), uid_from_database)

                                self.dmlutil.do_sql(each_update_sql_strend)
                            else:
                                pass

                        else:
                            # 说明trend表中没有对应记录，需要插入全新数据
                            each_insert_sql_strend = "insert into blw_upfanstrend(mid,watch_times,fans_now,last_update) " \
                                                     "values(%d, 1, %d, '%s')" % (uid_from_database,
                                                                                  fans,
                                                                                  timeutil.get_now_date())
                            self.dmlutil.do_sql(each_insert_sql_strend)

                except Exception as e:
                    self.logger.error('出现异常：' + str(e))


                trend_deal_end_time = timeutil.get_now_datetime()
                self.logger.info('****************************trend表处理耗时：%s'
                                 '****************************' % timeutil.date_diff(trend_deal_begin_time,
                                                                                     trend_deal_end_time))
                print('****************************trend表处理耗时：%s'
                      '****************************' % timeutil.date_diff(trend_deal_begin_time,
                                                                          trend_deal_end_time))

            watch_end_time = timeutil.get_now_datetime()
            self.logger.info('****************************三表处理耗时：%s'
                             '****************************' % timeutil.date_diff(watch_begin_time, watch_end_time))
            print('****************************三表处理耗时：%s'
                  '****************************' % timeutil.date_diff(watch_begin_time, watch_end_time))

            # 批量执行sql
            '''不能批量放在循环外批量执行，第三张表strend需要用到前两张表的数据，如果放在循环外批量执行sql，则循环内处理第三张表会出现问题'''
            # dmlutil.batch_do_sql(update_sql)  # 更新 blw_watchlist 表
            # dmlutil.batch_do_sql(insert_sql_record) # 在 blw_upfansrecord 表中添加粉丝记录

            '''记录日志'''
            loop_10_end = timeutil.get_now_datetime()
            self.logger.info('$$$$$$$$$$$$$$$$$$$$$$$$$$$$第%d次10循耗时：%s'
                             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$' % ((i + 1), timeutil.date_diff(loop_10_begin, loop_10_end)))
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$第%d次10循耗时：%s'
                  '$$$$$$$$$$$$$$$$$$$$$$$$$$$$' % ((i + 1), timeutil.date_diff(loop_10_begin, loop_10_end)))

        loop_end_time = timeutil.get_now_datetime()
        self.logger.info("############################本次处理结束,处理耗时:%s"
                         "############################" % timeutil.date_diff(loop_begin_time, loop_end_time))
        print("############################本次处理结束,处理耗时:%s"
              "############################" % timeutil.date_diff(loop_begin_time, loop_end_time))

    # 预测up主主投频道，记录up主所有频道投稿数
    def forecast_up_channel(self, json_channel_response):
        # channel_response = self.biliapi.get_up_channel(uid)
        # json_channel_response = json.loads(channel_response)
        tlist = json_channel_response.get('data').get('list').get('tlist')
        insert_blw_channel_sql_list = []
        max_tid = None
        max_count = 0
        tid_count_list = []
        for i in tlist.values():

            tid = i.get('tid')
            count = i.get('count')
            tid_count_list.append({tid: count})  # 将tid添加到up主的tidlist中
            tname = i.get('name')

            # 获取投稿最多的频道
            if max_count < count:
                max_count = count
                max_tid = tid

            # 查询blw_channel表中是否有该频道的信息,如果有，则忽略，如果没有，则添加
            query_is_exist_channel_sql = 'select count(tid) from blw_channel where tid = %d' % tid
            is_exist_channel_rs = self.dmlutil.query_sql(query_is_exist_channel_sql)
            if is_exist_channel_rs.data[0][0] == 0:
                insert_blw_channel_sql_list.append("insert into blw_channel(tid,tname) values (%d, '%s')"
                                                   % (tid, tname))
        self.dmlutil.batch_do_sql(insert_blw_channel_sql_list)

        return tid_count_list, max_tid
