# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
import logging
from django.db.transaction import atomic
from django.db import connections
from django.contrib.auth.views import login,logout,login_required,auth_login
from models.models_inception import  information_schema,tb_review,tb_review_history
import datetime as dtime
from django.core.mail import send_mail


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='data_manage.log',
                    filemode='a')


today=dtime.date.today()
oneday=dtime.timedelta(days=1)
yesterday=today-oneday

date = "%s 00:00:00" % (today)

from_email='changyanlong@soyoung.com'

@login_required()
def reviewReport(request):
    '''审核内容上报'''
    try:
        if request.method == "GET" and request.user.is_superuser == 0:
            username = request.user.username
            sql_sum = '''select count(*) from tb_review where flag=1 and create_time >date_format(now(),'%Y-%m-%d 00:00:00') '''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_sum = '''select id,db_tag from tb_databases_config'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            datarows = cursor.fetchall()
            dict_report = {}
            dict_report['user'] = username
            dict_report['taskCount'] = sum_row
            dict_report['database'] = datarows
            return render(request, 'review/report.html', context=dict_report)
        else:
            return render(request, 'review/404.html',context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/404.html',context=None)


@login_required()
@atomic()
def reviewReportActive(request):
    try:
        if request.method == "POST" and request.user.is_superuser == 0:
            # 1、获取上报内容
            select = request.POST.getlist('select[]',None)
            content = request.POST.get('text',None)
            userid = request.user.id
            leng = len(select)
            title = '''SQL审核通知！'''
            message = '''用户{0}已提交新的SQL，请尽快审核！'''.format(request.user.username)
            if leng > 1:
                for i in range(len(select)):
                    review_report = tb_review(database_id=select[i], content=content, creator=userid, flag=0,
                                              review_id=0)
                    review_report.save(using='default')
                    send_mail(title, message, from_email,
                              ['changyanlong@soyoung.com'], fail_silently=True)
                return write(1)
            elif leng == 1:
                review_report = tb_review(database_id=select[0],content=content,creator=userid,flag=0,review_id=0)
                review_report.save(using='default')
                send_mail(title, message, from_email=from_email,
                          recipient_list=['changyanlong@soyoung.com'],fail_silently=True)
                return write(1)
            else:
                return write(0)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception, e:
        logging.error(e)
        req = 0
        return write(req)


@login_required()
def reviewReportList(request):
    '''审核内容上报列表'''
    try:
        print request.method
        if request.method == "GET" and request.user.is_superuser == 0:
            userid = request.user.id
            username = request.user.username
            sql_sum = '''select count(*) from tb_review where flag=1 and create_time>date_format(now(),'%Y-%m-%d 00:00:00')'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql = '''SELECT 
                    a.id,
                    b.db_name,
                    a.content,
                    a.create_time,
                    a.flag,
                    a.review_time,
                    a.remarks
                FROM
                    tb_review as a left join tb_databases_config as b
                    on a.database_id=b.auto_id
                WHERE
                    a.creator = {0} and a.create_time>date_format(now(),'%Y-%m-%d 00:00:00')''' .format(userid)
            cursor = connections['default'].cursor()
            cursor.execute(sql)
            row = cursor.fetchall()
            dict_report = {}
            dict_report['reportlist'] = row
            dict_report['user'] = username
            dict_report['taskCount'] = sum_row
            return render(request, 'review/report_list.html', context=dict_report)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)


@login_required()
def reportUpdate(request):
    '''审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_superuser == 0:
            username = request.user.username
            sql_id = request.GET.get('sqlid',None)
            sql_sum = '''select count(*) from tb_review where flag=1 and create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_content = '''select id,content from tb_review where id = {0}''' .format(sql_id)
            cursor = connections['default'].cursor()
            cursor.execute(sql_content)
            content = cursor.fetchone()
            dict_report = {}
            dict_report['content'] = content
            dict_report['user'] = username
            dict_report['taskCount'] = sum_row
            return render(request, 'review/report_update.html', context=dict_report)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)


@login_required()
def reportUpdatePost(request):
    '''审核内容上报列表'''
    try:
        print request.method
        if request.method == "POST" and request.user.is_superuser == 0:
            sid = request.POST.get('sid',None)
            content = request.POST.get('text',None)
            print "%s,%s" % (sid,content)
            ct = tb_review.objects.get(id=sid)
            ct.content=content
            ct.flag=0
            ct.save()
            return write(1)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)




@login_required()
def reviewReportHistory(request):
    '''审核内容历史列表'''
    try:
        if request.method == "GET" and request.user.is_superuser == 0:
            userid = request.user.id
            username = request.user.username
            sql_sum = '''select count(*) from tb_review where create_time>date_format(now(),'%Y-%m-%d 00:00:00')'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql = '''SELECT a.id,b.db_name,a.content,a.create_time,a.flag,a.review_time,a.remarks  FROM  tb_review a left join tb_databases_config as b
                    on a.database_id=b.auto_id
                WHERE
                    a.creator={0}  and a.create_time<date_format(now(),'%Y-%m-%d 00:00:00') '''.format(
                userid)
            cursor = connections['default'].cursor()
            cursor.execute(sql)
            row = cursor.fetchall()
            dict_report = {}
            dict_report['reportlist'] = row
            dict_report['user'] = username
            dict_report['taskCount'] = sum_row
            return render(request, 'review/report_history.html', context=dict_report)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)