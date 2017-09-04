# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render
import logging,sys
from django.contrib import auth
from django.db import connections
from django.contrib.auth.views import login_required
from django.db.transaction import atomic
from django.contrib.auth.hashers import make_password, check_password
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='data_manage.log',
                    filemode='a')

@login_required()
def userPofile(request):
    '''用户页'''
    try:

        if request.method == "GET":
            sql_sum = '''select count(*) from tb_review where flag=0 and create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_database = '''select id,db_tag from tb_databases_config'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_database)
            data_row = cursor.fetchall()
            name = request.user.username
            dict = {}
            dict['user'] = name
            dict['taskCount'] = sum_row
            dict['database'] = data_row
            return render(request, 'review/user_profile_update.html', context=dict)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)


@login_required()
@atomic()
def userPofileUpdate(request):
    try:
        print request.method
        if request.method == 'POST':
            password = request.POST.get('password',None)
            email = request.POST.get('email',None)
            confirm = request.POST.get('confirm',None)
            print "%s,%s,%s" % (confirm,email,password)

            if confirm == password:
                print '1'
                hash_passwd = make_password(confirm)
                print hash_passwd
                id = request.user.id
                print id
                sql = '''update auth_user set email="{0}",password="{1}" where id={2}''' .format(email,hash_passwd,id)
                print sql
                cursor = connections['default'].cursor()
                cursor.execute(sql)
                sql_sum = '''select count(*) from tb_review where flag=0 and create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
                cursor = connections['default'].cursor()
                cursor.execute(sql_sum)
                sum_row = cursor.fetchone()
                sql_database = '''select id,db_tag from tb_databases_config'''
                cursor = connections['default'].cursor()
                cursor.execute(sql_database)
                data_row = cursor.fetchall()
                name = request.user.username
                dict = {}
                dict['flag'] = 1
                dict['user'] = name
                dict['taskCount'] = sum_row
                dict['database'] = data_row
                return render(request, 'review/user_profile_update.html', context=dict)
            else:
                sql_sum = '''select count(*) from tb_review where flag=0 and create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
                cursor = connections['default'].cursor()
                cursor.execute(sql_sum)
                sum_row = cursor.fetchone()
                sql_database = '''select id,db_tag from tb_databases_config'''
                cursor = connections['default'].cursor()
                cursor.execute(sql_database)
                data_row = cursor.fetchall()
                name = request.user.username
                dict = {}
                dict['flag'] = 0
                dict['user'] = name
                dict['taskCount'] = sum_row
                dict['database'] = data_row
                return render(request, 'review/user_profile_update.html', context=dict)
        else:
            return render(request, 'review/500.html', context=None)
    except Exception,e:
        logging.info(e)
        return write(0)