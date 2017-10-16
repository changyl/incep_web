# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render
from django.db import connections
from django.contrib.auth.views import login_required
import collections,json,datetime,sys,logging
from baseTools import getUserInfo_01

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='incption_web.log',
                    filemode='a')

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

@login_required()
def auditHistoryList(request):
    '''所有审核内容上报历史'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            result = getUserInfo_01(username=request.user.username,userid=request.user.id)
            return render(request, 'review/review_history_02.html', context=result)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)



@login_required()
def auditHistoryListDate(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            start = 0
            length = 0
            sumcnt = 0
            draw = request.GET.get('draw',None)
            start = request.GET.get('start',None)
            length = request.GET.get('length',None)
            sql_sum ='''select count(*) from tb_review where  create_time <date_format(now(),'%Y-%m-%d 00:00:00')'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_history_date = '''SELECT t.id,t.name,t.db_name,t.content,t.flag,t.review_time, uu.username,t.remark_user  FROM (SELECT  u.username as name, d.db_name,  r.id,r.content,  r.flag, r.remarks, r.review_time, r.review_id,r.remark_user FROM auto_database.tb_review r, tb_databases_config d, auth_user u  WHERE r.database_id = d.id and  r.creator = u.id AND r.creator = {0} and r.create_time <date_format(now(),'%Y-%m-%d 00:00:00')) AS t LEFT JOIN auth_user uu ON t.review_id = uu.id order by t.id desc  limit {1},{2}''' .format(request.user.id,start,length)
            cursor = connections['default'].cursor()
            cursor.execute(sql_history_date)
            all_row = cursor.fetchall()
            dict = collections.OrderedDict()
            dict['draw'] = draw
            dict['recordsTotal'] = sum_row[0]
            dict['recordsFiltered'] = sum_row[0]
            dict['data'] = all_row
            json_object = json.dumps(dict,cls=DateEncoder)
            return write(json_object)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)