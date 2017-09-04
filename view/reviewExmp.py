# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
import logging
from django.db import connections
from django.contrib.auth.views import login,logout,login_required,auth_login
import time,collections,json,datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='data_manage.log',
                    filemode='a')

@login_required()
def reviewUseExamp(request):
    '''所有审核内容上报列表'''
    try:
        print request.user.is_superuser
        if request.method == "GET" and request.user.is_superuser == 0:
            name = request.user.username
            sql_sum = '''select count(*) from tb_review where flag=1'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            dict = {}
            dict['name'] = name
            dict['taskCount'] = sum_row
            return render(request, 'review/user_examp.html', context=dict)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)
