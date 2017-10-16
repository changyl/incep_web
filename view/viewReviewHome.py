# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
import logging,collections,json,sys,decimal
from django.db import connections
from django.contrib.auth.views import login,logout,login_required,auth_login
from django.contrib import auth
import datetime as dtime
from baseTools import getUserType
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='data_manage.log',
                    filemode='a')




class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

@login_required
def loginHome(request):
    try:
        user_type = getUserType(request)
        # sql = '''select * from coolqi_menus'''
        # menu_1 = menus.objects.filter(parent_id = 0).order_by('sort').all()
        # menu_2 = menus.objects.filter(~Q(parent_id = 0)).all()
        username = request.user.username
        if user_type == 1:
            dict_1 = {}
            sql_sum = '''select count(*) from tb_review where flag=0 and create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_order = '''SELECT 
                                cnt, username, (@rowno:=@rowno + 1) AS no
                            FROM
                                (SELECT 
                                    COUNT(*) AS cnt, u.username
                                FROM
                                    auto_database.tb_review AS t
                                LEFT JOIN auth_user AS u ON t.creator = u.id
                                GROUP BY t.creator) c,
                                (SELECT (@rowno:=0)) b
                            ORDER BY c.cnt DESC limit 10;'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_order)
            order = cursor.fetchall()
            dict_1['taskCount'] = sum_row
            dict_1['user'] = username
            dict_1['order'] = order
            return render(request,'review/index_custom.html',context=dict_1)
        else:
            dict_1 = {}
            sql_sum = '''select count(*) from tb_review where (flag=0 or flag=1) and creator={0} and create_time >date_format(now(),'%Y-%m-%d 00:00:00')''' .format(request.user.id)
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            dict_1['taskCount'] = sum_row
            dict_1['user'] = username
            return render(request, 'review/index.html', context=dict_1)
    except Exception,e:
        logging.error(e)

@login_required
def index_char_pie(request):
    try:
        user_type = getUserType(request)
        if user_type == 1 and request.method == "POST":
            sql_stat = '''select sum(deleting) del,sum(inserting) as ins,sum(updating) as upd from statistic'''
            cursor = connections['data_backup'].cursor()
            cursor.execute(sql_stat)
            sum_stat = cursor.fetchone()
            dict = collections.OrderedDict()
            dict['stat'] = sum_stat
            json_object = json.dumps(dict, cls=DecimalEncoder)
            return write(json_object)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.info(e)

@login_required
def index_char_pie_ddl(request):
    try:
        if request.user.is_staff == 1 and request.method == "POST":
            sql_stat = '''select
                                SUM(altertable) AS altab,
                                SUM(renaming) AS renm,
                                SUM(createindex) AS cidx,
                                SUM(dropindex) AS didx,
                                SUM(addcolumn) AS addc,
                                SUM(changecolumn) AS chgc,
                                SUM(createtable) AS ctab,
                                SUM(truncating) AS tcat
                            from
                                statistic;'''
            cursor = connections['data_backup'].cursor()
            cursor.execute(sql_stat)
            sum_stat = cursor.fetchone()
            print sum_stat
            dict = collections.OrderedDict()
            dict['stat'] = sum_stat
            json_object = json.dumps(dict, cls=DecimalEncoder)
            return write(json_object)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception, e:
        logging.info(e)

@login_required
def index_char_line(request):
    try:
        if request.user.is_staff == 1 and request.method == "POST":
            sql_stat = '''SELECT 
                        *
                    FROM
                        (SELECT 
                            amount, DATE_FORMAT(data_date, '%Y-%m-%d') dt
                        FROM
                            auto_database.tb_review_stat
                        ORDER BY create_date DESC
                        LIMIT 7) t
                    ORDER BY t.dt ASC'''
            print sql_stat
            cursor = connections['default'].cursor()
            cursor.execute(sql_stat)
            sum_stat = cursor.fetchall()
            dict = collections.OrderedDict()
            dict['stat'] = sum_stat
            json_object = json.dumps(dict, cls=DecimalEncoder)
            return write(json_object)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception, e:
        logging.info(e)





#登录页面
def reviewUserLogin(request):
    try:
        dict = {}
        dict['status'] = "hide"
        return render(request, 'review/login.html', context=dict)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html', context=None)


def reviewUserLoginVerification(request):
    '''登录认证'''
    try:
        if request.method == "POST":
            #1、获取登录用户和密码
            username = request.POST.get('user',None)
            password = request.POST.get('passwd',None)
            print username,password
            uname = auth.authenticate(username=username, password=password)

            #判断用户和密码
            if uname is not None and uname.is_active:
                auth.login(request, uname)
                return redirect('/')
            else:
                dict = {}
                dict['status'] = ""
                return render(request, 'review/login.html', context=dict)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)

@login_required()
def reviewUserLogout(request):
    '''退出登录'''
    try:
        #1、登录用户退出登录
        logout(request)
        return redirect('/')
        # return render(request, 'review/login.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)



