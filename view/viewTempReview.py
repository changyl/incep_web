# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
import logging
from django.db.transaction import atomic
from django.db import connections
from django.contrib.auth.views import login,logout,login_required,auth_login
import datetime as dtime
import sys,MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='data_manage.log',
                    filemode='a')

today=dtime.date.today()
oneday=dtime.timedelta(days=1)
yesterday=today-oneday

date = "%s 00:00:00" % (today)


@login_required()
def reviewTemp(request):
    '''临时审核页列表'''
    try:
        if request.method == "GET" and request.user.is_superuser == 1:
            sql_sum = '''select count(*) from tb_review where flag=0 and create_time >date_format(now(),'%Y-%m-%d 00:00:00')''' .format(date)
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_database = '''select id,db_tag from tb_databases_config'''.format(date)
            cursor = connections['default'].cursor()
            cursor.execute(sql_database)
            data_row = cursor.fetchall()
            name = request.user.username
            dict = {}
            dict['user'] = name
            dict['taskCount'] = sum_row
            dict['database'] = data_row
            return render(request, 'review/review.html', context=dict)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)

@login_required()
@atomic()
def reviewTempActive(request):
    try:
        if request.method == "POST" and request.user.is_superuser == 1:
            # 1、获取审核内容
            select = request.POST.getlist('select',None)
            content = request.POST.get('text',None)
            userid = request.user.id

            #2、获取审核目标数据库信息
            sql_database_info = '''select host,user,passwd,port,db_name,creator from tb_databases_config where id={0}'''.format(
                select[0])

            cursor = connections['default'].cursor()
            cursor.execute(sql_database_info)
            row = cursor.fetchone()
            cursor.close()
            #3、执行审核
            target_sql = '''/*--user={0};--password={1};--host={2};--execute=1;--enable-ignore-warnings;--port={3};*/'''.format(
                row[1], row[2], row[0], row[3])
            db_sql = '''use {0};'''.format(row[4])
            ct = content.replace('"', '\'')
            ddl_dml_sql = '''{0}'''.format(ct)
            main_sql = '''{0}inception_magic_start;{1}{2} inception_magic_commit;'''.format(target_sql, db_sql,
                                                                                            ddl_dml_sql)
            conn = MySQLdb.connect(host='172.16.16.20', user='root', passwd='', db='', port=6669)
            cur = conn.cursor()
            cur.execute(main_sql.encode('utf-8'))
            results = cur.fetchall()
            cur.close()
            # print results
            # column_name_max_size = max(len(i[0]) for i in cur.description)
            # row_num = 0
            # # stagestatus = ''
            # res = ''
            # for result in results:
            #     row_num = row_num + 1
            #     print '*'.ljust(27, '*'), row_num, '.row', '*'.ljust(27, '*')
            #     rows = map(lambda x, y: (x, y), (i[0] for i in cur.description), result)
            #     for each_column in rows:
            #         if each_column[0] != 'errormessage':
            #             q = each_column[0].rjust(column_name_max_size),":",each_column[1]
            #
            #         else:
            #             q = res+each_column[0].rjust(column_name_max_size), ':', each_column[1].replace('\n', '\n'.ljust(
            #                 column_name_max_size + 4))
            cur.close()
            conn.close()

            return write(results)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception, e:
        logging.error(e)
        req = 0
        return write(req)