# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
import logging,collections,json,sys,decimal
from django.db import connections
from django.contrib.auth.views import login,logout,login_required,auth_login
from django.contrib import auth
import datetime as dtime
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='data_manage.log',
                    filemode='a')


@login_required()
def reviewRollBack(request):
    try:
        if request.method == 'POST' and request.user.is_superuser == 1:
            x_id = request.POST.get('xlh',None)
            db_bak = request.POST.get('db_bak',None)
            sql_id = request.POST.get('sql_id',None)
            sql_1 = '''select tablename from {0}.$_$Inception_backup_information$_$ where opid_time={1};''' .format(db_bak,x_id)
            cursor = connections['data_backup'].cursor()
            cursor.execute(sql_1)
            row_1 = cursor.fetchone()
            sql_2 = '''select rollback_statement from {0}.{1} where opid_time={2};''' .format(db_bak,row_1[0],x_id)
            cursor = connections['data_backup'].cursor()
            cursor.execute(sql_2)
            row_2 = cursor.fetchone()
            rollback(sqlid=sql_id,content=row_2[0])
            return write(1)
        else:
            return render(request, 'review/500.html', context=None)
    except Exception,e:
        logging.info(e)
        return write(0)


def rollback(sqlid,content):
    '''执行回滚语句'''
    try:
        sql_dt_id = '''select database_id from tb_review where id={0}''' .format(sqlid)
        print sql_dt_id
        cursor = connections['default'].cursor()
        cursor.execute(sql_dt_id)
        row1 = cursor.fetchone()
        print row1
        sql_database_info  =  '''select host,user,passwd,port,db_name from tb_databases_config where id={0}'''.format(row1[0])
        print  sql_database_info
        cursor = connections['default'].cursor()
        cursor.execute(sql_database_info)
        row2 = cursor.fetchone()
        logging.debug(sql_database_info)
        print row2
        sql = '''{0}''' .format(content)
        print sql
        conn = MySQLdb.connect(host=row2[0], user=row2[1], passwd=row2[2], db=row2[4], port=row2[3])
        cur = conn.cursor()
        cur.execute(sql.encode('utf-8'))
        result = conn.commit()
        return result
    except Exception,e:
        logging.error(e)



