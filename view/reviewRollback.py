# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
import logging
from django.db.transaction import atomic
from django.db import connections
from django.contrib.auth.views import login,logout,login_required,auth_login
from models.models_inception import  information_schema,tb_databases_config,tb_review,tb_review_history
import datetime as dtime
import time,collections,json,datetime
import MySQLdb,sys
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


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


@login_required()
def reviewRoballBackup(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_superuser == 1:
            name = request.user.username
            sql_sum = '''select count(*) from tb_review where flag=0 and create_time >"{0}"''' .format(date)
            sql_schema = '''select TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME,TABLE_ROWS 
                          from information_schema.TABLES 
                          where TABLE_SCHEMA like '1%' and TABLE_NAME not like '%backup%';'''
            cursor = connections['data_backup'].cursor()
            cursor.execute(sql_sum)
            sum = cursor.fetchall()
            cursor = connections['data_backup'].cursor()
            cursor.execute(sql_schema)
            rows = cursor.fetchall()
            dict = {}
            dict['name'] = name
            dict['taskCount'] = sum
            dict['rows'] = rows
            return render(request, 'review/review_roball_backup.html', context=dict)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)


@login_required()
def reviewPostRoballBackup(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_superuser == 1:
            start = 0
            length = 0
            sumcnt = 0
            draw = request.GET.get('draw',None)
            start = request.GET.get('start',None)
            length = request.GET.get('length',None)
            sql_sum ='''select count(*) from tb_review where  create_time <"{0}"''' .format(date)
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_arry = '''SELECT t.id,t.name,t.db_name,t.content,t.flag,t.review_time, uu.username  FROM (SELECT  u.username as name, d.db_name,  r.id,r.content,  r.flag, r.remarks, r.review_time, r.review_id FROM auto_database.tb_review r, tb_databases_config d, auth_user u  WHERE r.database_id = d.id AND r.creator = u.id and r.create_time <"{0}") AS t LEFT JOIN auth_user uu ON t.review_id = uu.id order by t.id desc  limit {1},{2}''' .format(date,start,length)
            print sql_arry
            cursor = connections['default'].cursor()
            cursor.execute(sql_arry)
            all_row = cursor.fetchall()
            dict = collections.OrderedDict()
            dict['draw'] = draw
            dict['recordsTotal'] = sum_row[0]
            dict['recordsFiltered'] = sum_row[0]
            dict['data'] = all_row
            json_object = json.dumps(dict,cls=DateEncoder)
            print json_object
            return write(json_object)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)
