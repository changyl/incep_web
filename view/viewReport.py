# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse as write
from django.shortcuts import render
from django.db.transaction import atomic
from django.contrib.auth.views import login_required
from baseTools import getUserInfo
from models.models_inception import  tb_review
import logging,sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='incption_web.log',
                    filemode='a')

reload(sys)
sys.setdefaultencoding('utf8')



@login_required()
def sqlReport(request):
    '''审核内容上报'''
    try:
        if request.method == "GET" and request.user.is_staff == 0:
            result = getUserInfo(username=request.user.username)
            return render(request, 'review/report.html', context=result)
        else:
            return render(request, 'review/404.html',context=None)
    except Exception,e:
        logging.error(e)


@login_required()
@atomic()
def sqlReportActive(request):
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
                    #em = sendEmail(title=title, message=message, from_email=from_email,to_email=to_email)
                    #em.send()
                return write(1)
            elif leng == 1:
                review_report = tb_review(database_id=select[0],content=content,remark_user=bak,creator=userid,flag=0,review_id=0)
                review_report.save(using='default')
                #em = sendEmail(title=title, message=message, from_email=from_email, to_email=to_email)
                #em.send()
                return write(1)
            else:
                return write(0)
    except Exception, e:
        logging.error(e)