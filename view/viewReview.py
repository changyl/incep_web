# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
from django.db.transaction import atomic
from django.db import connections
from django.contrib.auth.views import login_required
from models.models_inception import  tb_databases_config,tb_review,tb_review_history
import datetime as dtime
import collections,json,datetime,sys,logging
from baseEmail import sendEmail
from baseTools import auditExecute,preAuditExecute,inceptionQuery,getUserInfo,getUserInfo_02

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
from_email='sqlaudit@soyoung.com'

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

@login_required()
def reviewReportListAll(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_superuser == 1:
            result = getUserInfo(username=request.user.username)
            return render(request, 'review/review_list_all.html', context=result)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)


@login_required()
def reviewPost(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_superuser == 1:
            start = 0
            length = 0
            sumcnt = 0
            draw = request.GET.get('draw',None)
            start = request.GET.get('start',None)
            length = request.GET.get('length',None)
            sql_sum ='''select count(*) from tb_review where  create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
            # print sql_sum
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_arry = '''select t.id,d.db_name,t.database_id,t.content,t.flag,t.create_time,t.username,t.remarks,t.remark_user from (SELECT r.id as id,database_id,content,create_time ,u.username,r.flag,r.remarks,r.remark_user  FROM  tb_review as r left join auth_user as u ON r.creator=u.id where  r.create_time>date_format(now(),'%Y-%m-%d 00:00:00') ) as t left join tb_databases_config d on t.database_id=d.id  order by t.id desc  limit {0},{1};''' .format(start,length)

            cursor = connections['default'].cursor()
            cursor.execute(sql_arry)
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




@login_required()
def reviewListAllHistory(request):
    '''所有审核内容上报历史'''
    try:
        if request.method == "GET" and request.user.is_superuser == 1:
            result = getUserInfo(username=request.user.username)
            return render(request, 'review/review_history.html', context=result)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)



@login_required()
def reviewPostHistory(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_superuser == 1:
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
            sql_arry = '''SELECT t.id,t.name,t.db_name,t.content,t.flag,t.review_time, uu.username,t.remark_user  FROM (SELECT  u.username as name, d.db_name,  r.id,r.content,  r.flag, r.remarks, r.review_time, r.review_id,r.remark_user FROM auto_database.tb_review r, tb_databases_config d, auth_user u  WHERE r.database_id = d.id AND r.creator = u.id and r.create_time <date_format(now(),'%Y-%m-%d 00:00:00')) AS t LEFT JOIN auth_user uu ON t.review_id = uu.id order by t.id desc  limit {0},{1}''' .format(start,length)
            cursor = connections['default'].cursor()
            cursor.execute(sql_arry)
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


@login_required()
@atomic()
def reviewPreExecute(request):
    '''内容预审核'''
    try:
        databaseid = int(request.POST.get('id',None))
        content = request.POST.get('content',None)
        sql_id = request.POST.get('sqlid',None)

        sql_database_info  =  '''select host,user,passwd,port,db_name,creator from tb_databases_config where id={0}'''.format(databaseid)
        cursor = connections['default'].cursor()
        cursor.execute(sql_database_info)
        row = cursor.fetchone()
        logging.debug(sql_database_info)
        audit_sql = preAuditExecute(user=row[1],password=row[2],host=row[0],port=row[3],dbname=row[4],content=content)

        if request.method == "POST" and request.user.is_superuser == 1:
            result = inceptionQuery(audit_sql)
            flag = []
            for row in result:
                flag.append(row[2])
                sql = '''REPLACE into tb_review_detail(tid,stage,errlevel,stagestatus,errormessage,`sql`,Affected_rows,sequence,backup_dbname,execute_time,sqlsha1,sql_id) values({0},"{1}",{2},"{3}","{4}","{5}",{6},"{7}","{8}","{9}","{10}",{11}) ;''' .format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql)
            cursor.close()
            return write(1)
        else:
            return write(0)
    except Exception,e:
        logging.error(e)



@login_required()
@atomic()
def reviewExecute(request):
    '''审核内容执行'''
    try:
        databaseid = int(request.POST.get('id',None))
        content = request.POST.get('content',None)
        creatorid = request.POST.get('creator', None)
        sql_id = request.POST.get('sqlid',None)

        sql_database_info  =  '''select host,user,passwd,port,db_name,creator from tb_databases_config where id={0}'''.format(databaseid)
        cursor = connections['default'].cursor()
        cursor.execute(sql_database_info)
        row = cursor.fetchone()
        logging.debug(sql_database_info)
        audit_sql = auditExecute(user=row[1],password=row[2],host=row[0],port=row[3],dbname=row[4],content=content)

        if request.method == "POST" and request.user.is_superuser == 1:
            result = inceptionQuery(audit_sql)
            flag = []
            for row in result:
                flag.append(row[2])
                sql = '''REPLACE into tb_review_detail(tid,stage,errlevel,stagestatus,errormessage,`sql`,Affected_rows,sequence,backup_dbname,execute_time,sqlsha1,sql_id) values({0},"{1}",{2},"{3}","{4}","{5}",{6},"{7}","{8}","{9}","{10}",{11}) ;''' .format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql)
            cursor.close()
            title = '''SQL审核通知！'''
            falis_message = '''sqlid为{0}的审核未通过！''' .format(sql_id)
            suss_message = '''sqlid为{0}的已审核通过！''' .format(sql_id)
            sql_to_eamil = '''select username from auth_user where id= (select creator from tb_review where id={0})''' .format(sql_id)
            cursor = connections['default'].cursor()
            cursor.execute(sql_to_eamil)
            re_to_uname = cursor.fetchone()
            to_email = '%s@soyoung.com' % re_to_uname
            if 2 in flag:
                sql_flag ='''update tb_review set flag=1,review_id={0},review_time=now() where id={1}''' .format(request.user.id,sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql_flag)
                em = sendEmail(title=title, message=falis_message, from_email=from_email, to_email=to_email)
                em.send()
                return write(0)
            else:
                sql_flag_02 = '''update tb_review set flag=2,review_id={0},review_time=now() where id={1}'''.format(request.user.id,sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql_flag_02)
                em = sendEmail(title=title, message=suss_message, from_email=from_email, to_email=to_email)
                em.send()
                return write(1)
        else:
            return write(0)
    except Exception,e:
        logging.error(e)


@login_required()
def reviewDetail(request):
    '''审核内容详情'''
    try:
        if request.method == "GET" and request.user.is_superuser == 1:
            sql_id = request.GET.get('sqlid',None)
            dict_report = getUserInfo_02(username=request.user.username,sql_id=sql_id)
            return render(request, 'review/review_detail.html', context=dict_report)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html', context=None)


@login_required()
def reviewBak(request):
    try:
        if request.method == 'POST' and request.user.is_superuser == 1:
            sql_id = request.POST.get('id',None)
            bak = request.POST.get('bak',None)
            res = tb_review.objects.get(id=sql_id)
            res.remarks=bak
            res.save()
            return write(1)
        else:
            return render(request, 'review/500.html', context=None)
    except Exception,e:
        logging.info(e)
        return render(request, 'review/404.html', context=None)