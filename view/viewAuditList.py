# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse as write
from django.shortcuts import render
from django.db.transaction import atomic
from django.contrib.auth.views import login_required
from django.db import connections
import logging,sys,datetime
import collections,json
from baseTools import fullExecute,preAuditExecute,inceptionQuery,getUserInfo_02,getUserInfo_01

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='incption_web.log',
                    filemode='a')

reload(sys)
sys.setdefaultencoding('utf8')

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


@login_required()
def sqlAuditList(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            result = getUserInfo_01(username=request.user.username,userid=request.user.id)
            return render(request, 'review/review_list_all_02.html', context=result)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)


@login_required()
def sqlAuditPost(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            start = 0
            length = 0
            sumcnt = 0
            draw = request.GET.get('draw',None)
            start = request.GET.get('start',None)
            length = request.GET.get('length',None)
            sql_sum ='''select count(*) from tb_review where  (flag=0 or flag=1)  and creator={0} and create_time >date_format(now(),'%Y-%m-%d 00:00:00')''' .format(request.user.id)
            # print sql_sum
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql_arry = '''select t.id,d.db_name,t.database_id,t.content,t.flag,t.create_time,t.username,t.remarks,t.remark_user from (SELECT r.id as id,database_id,content,create_time ,u.username,r.flag,r.remarks,r.remark_user  FROM  tb_review as r left join auth_user as u ON r.creator=u.id where  r.create_time>date_format(now(),'%Y-%m-%d 00:00:00') AND r.creator = {0} ) as t left join tb_databases_config d on t.database_id=d.id  order by t.id desc  limit {1},{2};''' .format(request.user.id,start,length)

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



@login_required()
@atomic()
def auditPreExecute(request):
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

        if request.method == "POST" and request.user.is_staff == 0:
            result = inceptionQuery(audit_sql)
            flag = []
            for row in result:
                flag.append(row[2])
                rep_str = row[5]
                strs = rep_str.replace("'","\\'")
                strss = strs.replace('"', "\\'")
                sql = '''REPLACE into tb_review_detail(tid,stage,errlevel,stagestatus,errormessage,`sql`,Affected_rows,sequence,backup_dbname,execute_time,sqlsha1,sql_id) values({0},"{1}",{2},"{3}","{4}",'{5}',{6},"{7}","{8}","{9}","{10}",{11}) ;''' .format(row[0],row[1],row[2],row[3],row[4],strss,row[6],row[7],row[8],row[9],row[10],sql_id)
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
def auditExecute(request):
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
        audit_sql = fullExecute(user=row[1],password=row[2],host=row[0],port=row[3],dbname=row[4],content=content)

        if request.method == "POST" and request.user.is_staff == 0:
            result = inceptionQuery(audit_sql)
            flag = []
            for row in result:
                flag.append(row[2])
                rep_str = row[5]
                strs = rep_str.replace("'", "\\'")
                strss = strs.replace('"', "\\'")
                sql = '''REPLACE into tb_review_detail(tid,stage,errlevel,stagestatus,errormessage,`sql`,Affected_rows,sequence,backup_dbname,execute_time,sqlsha1,sql_id) values({0},"{1}",{2},"{3}","{4}","{5}",{6},"{7}","{8}","{9}","{10}",{11}) ;''' .format(row[0],row[1],row[2],row[3],row[4],strss,row[6],row[7],row[8],row[9],row[10],sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql)
            cursor.close()
            if 2 in flag or 1 in flag:
                sql_flag ='''update tb_review set flag=1,review_id={0},review_time=now() where id={1}''' .format(request.user.id,sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql_flag)
                return write(0)
            else:
                sql_flag_02 = '''update tb_review set flag=2,review_id={0},review_time=now() where id={1}'''.format(request.user.id,sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql_flag_02)
                return write(1)
        else:
            return write(0)
    except Exception,e:
        logging.error(e)


@login_required()
def auditDetail(request):
    '''审核内容详情'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            sql_id = request.GET.get('sqlid',None)
            dict_report = getUserInfo_02(username=request.user.username,sql_id=sql_id,userid=request.user.id)
            return render(request, 'review/review_detail_02.html', context=dict_report)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html', context=None)
