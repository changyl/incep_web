# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render
from django.db import connections
from django.contrib.auth.views import login_required
import sys,logging
from models.models_inception import  tb_review

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='incption_web.log',
                    filemode='a')


@login_required()
def sqlUpdate(request):
    '''审核内容更新渲染展示'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            username = request.user.username
            sql_id = request.GET.get('sqlid',None)
            sql_sum = '''select count(*) from tb_review where flag=0 and create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_content = '''select id,content,remark_user from tb_review where id = {0}''' .format(sql_id)
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
def sqlUpdateActive(request):
    '''审核内容更新'''
    try:
        print request.method
        if request.method == "POST" and request.user.is_staff == 0:
            sid = request.POST.get('sid',None)
            content = request.POST.get('text',None)
            bak = request.POST.get('bak',None)
            ct = tb_review.objects.get(id=sid)
            ct.content=content
            ct.remark_user=bak
            ct.flag=0
            ct.save()
            return write(1)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)