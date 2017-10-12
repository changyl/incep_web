# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
import logging,sys
from django.db.transaction import atomic
from django.contrib.auth.views import login_required
from models.models_inception import  tb_review,tb_review_history
from django.db import connections
from baseTools import getUserInfoReport,getUserInfoReport_02
from baseEmail import sendEmail
from baseTools import Execute,preAuditExecute,inceptionQuery,getUserInfo,getUserInfo_02

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='data_manage.log',
                    filemode='a')


reload(sys)
sys.setdefaultencoding('utf8')


@login_required()
def reviewReport(request):
    '''审核内容上报'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            result = getUserInfoReport(username=request.user.username)
            return render(request, 'review/report.html', context=result)
        else:
            return render(request, 'review/404.html',context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/404.html',context=None)


@login_required()
@atomic()
def reviewReportActive(request):
    try:
        if request.method == "POST" and request.user.is_staff == 0:
            # 1、获取上报内容
            select = request.POST.getlist('select[]',None)
            content = request.POST.get('text',None)
            bak = request.POST.get('text2',None)
            userid = request.user.id
            leng = len(select)
            title = '''SQL审核通知！'''
            message = '''用户{0}已提交新的SQL，请尽快审核！'''.format(request.user.username)
            if leng > 1:
                for i in range(len(select)):
                    review_report = tb_review(database_id=select[i], content=content,remark_user=bak, creator=userid, flag=0,
                                              review_id=0)
                    review_report.save(using='default')
                    em = sendEmail(title=title, message=message, from_email=from_email,to_email=to_email)
                    em.send()
                return write(1)
            elif leng == 1:
                review_report = tb_review(database_id=select[0],content=content,remark_user=bak,creator=userid,flag=0,review_id=0)
                review_report.save(using='default')
                em = sendEmail(title=title, message=message, from_email=from_email, to_email=to_email)
                em.send()
                return write(1)
            else:
                return write(0)
    except Exception, e:
        logging.error(e)


# @login_required()
# def reviewReportList(request):
#     '''审核内容上报列表'''
#     try:
#         print request.method
#         if request.method == "GET" and request.user.is_staff == 0:
#             userid = request.user.id
#             result = getUserInfoReport_02(userid=userid,username=request.user.username)
#             return render(request, 'review/report_list.html', context=result)
#         else:
#             return render(request, 'review/404.html', context=None)
#     except Exception,e:
#         logging.error(e)
#         return render(request, 'review/500.html',context=None)




@login_required()
def reportUpdate(request):
    '''审核内容更新渲染展示'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            username = request.user.username
            sql_id = request.GET.get('sqlid',None)
            sql_sum = '''select count(*) from tb_review where flag=1 and create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
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
def reportUpdatePost(request):
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
        return render(request, 'review/500.html',context=None)




@login_required()
def reviewReportList(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            result = getUserInfo(username=request.user.username)
            return render(request, 'review/review_list_all_02.html', context=result)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)


@login_required()
def reportPost(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
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

        if request.method == "POST" and request.user.is_staff == 0:
            result = inceptionQuery(audit_sql)
            flag = []
            for row in result:
                flag.append(row[2])
                rep_str = row[5]
                strs = rep_str.replace("'","\\'")
                strss = strs.replace('"', "\\'")
                sql = '''REPLACE into tb_review_detail(tid,stage,errlevel,stagestatus,errormessage,`sql`,Affected_rows,sequence,backup_dbname,execute_time,sqlsha1,sql_id) values({0},"{1}",{2},"{3}","{4}",'{5}',{6},"{7}","{8}","{9}","{10}",{11}) ;''' .format(row[0],row[1],row[2],row[3],row[4],strss,row[6],row[7],row[8],row[9],row[10],sql_id)
                print sql
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
            title = '''SQL审核通知！'''
            #falis_message = '''sqlid为{0}的审核未通过！''' .format(sql_id)
            #suss_message = '''sqlid为{0}的已审核通过！''' .format(sql_id)
            #sql_to_eamil = '''select username from auth_user where id= (select creator from tb_review where id={0})''' .format(sql_id)
            cursor = connections['default'].cursor()
            cursor.execute(sql_to_eamil)
            re_to_uname = cursor.fetchone()
            #to_email = '%s@soyoung.com' % re_to_uname
            if 2 in flag:
                sql_flag ='''update tb_review set flag=1,review_id={0},review_time=now() where id={1}''' .format(request.user.id,sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql_flag)
                #em = sendEmail(title=title, message=falis_message, from_email=from_email, to_email=to_email)
                #em.send()
                return write(0)
            else:
                sql_flag_02 = '''update tb_review set flag=2,review_id={0},review_time=now() where id={1}'''.format(request.user.id,sql_id)
                cursor = connections['default'].cursor()
                cursor.execute(sql_flag_02)
                #em = sendEmail(title=title, message=suss_message, from_email=from_email, to_email=to_email)
                #em.send()
                return write(1)
        else:
            return write(0)
    except Exception,e:
        logging.error(e)


@login_required()
def reviewDetail(request):
    '''审核内容详情'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            sql_id = request.GET.get('sqlid',None)
            dict_report = getUserInfoReport_02(username=request.user.username,sql_id=sql_id)
            return render(request, 'review/review_detail.html', context=dict_report)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html', context=None)



@login_required()
def reviewReportHistory(request):
    '''审核内容历史列表'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            userid = request.user.id
            username = request.user.username
            sql_sum = '''select count(*) from tb_review where create_time>date_format(now(),'%Y-%m-%d 00:00:00')'''
            cursor = connections['default'].cursor()
            cursor.execute(sql_sum)
            sum_row = cursor.fetchone()
            sql = '''SELECT a.id,b.db_name,a.content,a.create_time,a.flag,a.review_time,a.remarks,a.remark_user  FROM  tb_review a 
                    left join tb_databases_config as b on a.database_id=b.auto_id WHERE
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