# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from xyz.badbugu.dbtool.dmlutil import DmlUtil
from xyz.badbugu.linutil import timeutil
from xyz.badbugu.scheduler.bilischeduler import BiliScheduler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def report_option():
    dmlUitl = DmlUtil()

    while True:

        print("############################报表############################")
        print("1. 观察列表")
        print("2. up主粉丝数排名")
        print("3. up主粉丝增长率排名（一天）")
        print("4. up主粉丝增长率排名（三天）")
        print("5. up主粉丝增长率排名（七天）")
        print("6. up主粉丝增长率排名（十五天）")
        print("7. up主粉丝增长率排名（一个月）")
        print("8. up主粉丝增长率排名（三个月）")
        print("9. up主粉丝增长率排名（六个月）")
        print("10. up主粉丝增长率排名（一年）")
        print("11. up主粉丝增长率排名（初始）")
        print('q. quit')
        print("############################报表############################")
        report_choose = input("请选择:")


        if report_choose == 'q':
            break

        report_choose_to_int = int(report_choose)
        if report_choose_to_int == 1:
            report_sql = 'select list.mid, ' \
                         'list.name, ' \
                         'list.sex, ' \
                         'list.level, ' \
                         'list.video_number, ' \
                         'list.begin_watch_date, ' \
                         'trend.watch_times ' \
                         'from blw_watchlist as list, blw_upfanstrend as trend ' \
                         'where list.mid = trend.mid'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################观察列表############################')
            print('  %10s  %20s  %20s  %20s  %20s  %25s  %20s ' % ('uid', '名字', '性别', '等级', '发布视频数', '开始观测时间', '观测次数'))
            for each in report_rs.data:
                try:
                    mid = each[0]
                    name = each[1]
                    sex = each[2]
                    if sex == 1:
                        sex = '男'
                    elif sex == 0:
                        sex = '女'
                    else:
                        sex = '未知'
                    level = each[3]
                    video_number = each[4]
                    begin_watch_date = each[5]
                    watch_times = each[6]

                    print('||%10s||%20s||%20s||%20s||%20s||%25s||%20s '
                          % (mid, name, sex, level, video_number,
                             timeutil.change_datetime_to_str(begin_watch_date),
                             watch_times))
                except AttributeError as e:
                    print(e)

        elif report_choose_to_int == 2:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by trend.fans_now desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################粉丝排名############################')
            print('%-20s%-s%+20s' % ('uid', '名字', '粉丝数'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]

                print('%-20s%-s%+20s' % (mid, name, fans_now))


        elif report_choose_to_int == 3:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now, ' \
                         'trend.fans_one, ' \
                         'trend.fans_rate1 ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by fans_rate1 desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（一天）############################')
            print('%-20s%-s%+20s%+20s' % ('名字', '粉丝数', '一天前粉丝数', '增长率'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_one = each[3]
                fans_rate1 = each[4]

                print('%-20s%-s%+20s%+20s%+20s%%' % (mid, name, fans_now, fans_one, fans_rate1))

        elif report_choose_to_int == 4:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now, ' \
                         'trend.fans_three, ' \
                         'trend.fans_rate2 ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by trend.fans_rate2 desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（三天）############################')
            # print('uid\t名字\t粉丝数\t三天前粉丝数')
            print('%-20s%-s%+20s%+20s' % ('名字', '粉丝数', '三天前粉丝数', '增长率'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_three = each[3]
                fans_rate2 = each[4]

                # print('%s\t%s\t%s\t%s\t' % (mid, name, fans_now, fans_three))
                print('%-20s%-s%+20s%+20s%+20s%%' % (mid, name, fans_now, fans_three, fans_rate2))

        elif report_choose_to_int == 5:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now, ' \
                         'trend.fans_seven, ' \
                         'trend.fans_rate3 ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by trend.fans_rate3 desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（七天）############################')
            # print('uid\t名字\t粉丝数\t七天前粉丝数')
            print('%-20s%-s%+20s%+20s' % ('名字', '粉丝数', '七天前粉丝数', '增长率'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_seven = each[3]
                fans_rate3 = each[4]

                # print('%s\t%s\t%s\t%s\t' % (mid, name, fans_now, fans_seven))
                print('%-20s%-s%+20s%+20s%+20s%%' % (mid, name, fans_now, fans_seven, fans_rate3))

        elif report_choose_to_int == 6:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now, ' \
                         'trend.fans_fifteen, ' \
                         'trend.fans_rate4 ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by trend.fans_rate4 desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（十五天）############################')
            # print('uid\t名字\t粉丝数\t十五天前粉丝数')
            print('%-20s%-s%+20s%+20s' % ('名字', '粉丝数', '十五天前粉丝数', '增长率'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_fifteen = each[3]
                fans_rate4 = each[4]

                # print('%s\t%s\t%s\t%s\t' % (mid, name, fans_now, fans_fifteen))
                print('%-20s%-s%+20s%+20s%+20s%%' % (mid, name, fans_now, fans_fifteen, fans_rate4))

        elif report_choose_to_int == 7:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now, ' \
                         'trend.fans_one_m, ' \
                         'trend.fans_rate5 ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by trend.fans_rate5 desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（一个月）############################')
            # print('uid\t名字\t粉丝数\t一个月前粉丝数')
            print('%-20s%-s%+20s%+20s' % ('名字', '粉丝数', '一个月前粉丝数', '增长率'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_one_m = each[3]
                fans_rate5 = each[4]

                # print('%s\t%s\t%s\t%s\t' % (mid, name, fans_now, fans_one_m))
                print('%-20s%-s%+20s%+20s%+20s%%' % (mid, name, fans_now, fans_one_m, fans_rate5))

        elif report_choose_to_int == 8:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now, ' \
                         'trend.fans_three_m, ' \
                         'trend.fans_rate6 ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by trend.fans_rate6 desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（三个月）############################')
            # print('uid\t名字\t粉丝数\t三个月前粉丝数')
            print('%-20s%-s%+20s%+20s' % ('名字', '粉丝数', '三个月前粉丝数', '增长率'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_three_m = each[3]
                fans_rate6 = each[4]

                # print('%s\t%s\t%s\t%s\t' % (mid, name, fans_now, fans_three_m))
                print('%-20s%-s%+20s%+20s%+20s%%' % (mid, name, fans_now, fans_three_m, fans_rate6))

        elif report_choose_to_int == 9:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now, ' \
                         'trend.fans_six_m, ' \
                         'trend.fans_rate7 ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by trend.fans_rate7 desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（六个月）############################')
            # print('uid\t名字\t粉丝数\t六个月前粉丝数')
            print('%-20s%-s%+20s%+20s' % ('名字', '粉丝数', '六个月前粉丝数', '增长率'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_six_m = each[3]
                fans_rate7 = each[4]

                # print('%s\t%s\t%s\t%s\t' % (mid, name, fans_now, fans_six_m))
                print('%-20s%-s%+20s%+20s%+20s%%' % (mid, name, fans_now, fans_six_m, fans_rate7))

        elif report_choose_to_int == 10:
            report_sql = 'select ' \
                         'trend.mid, ' \
                         'list.name, ' \
                         'trend.fans_now, ' \
                         'trend.fans_one_y, ' \
                         'trend.fans_rate8 ' \
                         'from blw_upfanstrend as trend , blw_watchlist as list ' \
                         'where trend.mid = list.mid ' \
                         'order by trend.fans_rate8 desc'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（一年）############################')
            # print('uid\t名字\t粉丝数\t一年前粉丝数')
            print('%-20s%-s%+20s%+20s' % ('名字', '粉丝数', '一年前粉丝数', '增长率'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_one_y = each[3]
                fans_rate8 = each[4]

                # print('%s\t%s\t%s\t%s\t' % (mid, name, fans_now, fans_one_y))
                print('%-20s%-s%+20s%+20s%+20s%%' % (mid, name, fans_now, fans_one_y, fans_rate8))

        elif report_choose_to_int == 11:
            report_sql = 'SELECT ' \
                         'trend.mid,' \
                         'list.`name`,' \
                         'trend.fans_now,' \
                         'trend.fans_compare_begin,' \
                         'trend.fans_rate9,' \
                         'record.watch_date ' \
                         'FROM blw_upfanstrend AS trend ' \
                         'LEFT JOIN ' \
                         '(SELECT mid,' \
                         'watch_date ' \
                         'FROM blw_upfansrecord GROUP BY mid HAVING MIN(watch_date)) AS record ' \
                         'ON trend.mid=record.mid ' \
                         'LEFT JOIN (select mid, `name` FROM blw_watchlist) AS list ON trend.mid = list.mid ' \
                         'ORDER BY trend.fans_rate9 DESC;'
            report_rs = dmlUitl.query_sql(report_sql)
            print('############################增长率排名（初始）############################')
            print('  %10s  %20s  %20s  %20s  %20s  %25s ' % ('uid', '名字', '粉丝数', '初始粉丝数', '增长率', '初始时间'))
            for each in report_rs.data:
                mid = each[0]
                name = each[1]
                fans_now = each[2]
                fans_compare_begin = each[3]
                fans_rate9 = each[4]
                watch_date_first = each[5]

                print('  %10s  %20s  %20s  %20s  %20s%%  %25s'
                      % (mid, name, fans_now, fans_compare_begin, fans_rate9,
                         watch_date_first))

        else:
            print('输入有误')


# 目前需要网页解析和网页下载器
# 网页解析器使用 beautifulsoop
# 网页下载器 ：urllib3
#

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('############################本次处理开始############################')
    while True:
        print('1.添加up主信息')
        print('2.开始爬取')
        print('3.报表')
        print('q.quit')
        choose = input('请选择：')
        if choose == '1':
            while True:
                mid = input('请输入up主mid(输入q退出)：')

                if mid == 'q':
                    break
                    
                # 查询表中是否有该uid
                select_watchlist_sql = 'select count(mid) from blw_watchlist where mid = %d' % int(mid)
                srs = DmlUtil().query_sql(select_watchlist_sql)
                if srs.data[0][0] == 1:
                    print('up主已经添加过了！')
                    continue

                description = input('请输入up描述：')

                insert_watchlist_sql = "insert into blw_watchlist(mid, add_date, description) values (%d, '%s', '%s')" \
                                       % (int(mid), timeutil.get_now_date(), description)
                rs = DmlUtil().do_sql(insert_watchlist_sql)
                if rs.data == 'OK':
                    print('插入成功！')
            print('添加完成!')
        elif choose == '2':
            print('爬取开始')
            bilischeduler = BiliScheduler()
            bilischeduler.begin_get_info()
            print('爬取完成')
        elif choose == '3':
            report_option()
        else:
            break
    print('############################本次处理结束############################')


