# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
import logging
import requests
from django.db.transaction import atomic
from django.db import connections
from django.contrib.auth.views import login,logout,login_required,auth_login
from django.contrib import auth
from models.models_inception import  information_schema,tb_databases_config,tb_review,tb_review_history
from django.db.models import Q
import time,collections,json,datetime
import MySQLdb


@login_required()
def test(request):
    '''所有审核内容上报列表'''
    try:
        if request.method == "GET" :
            userid = request.user.id
            return render(request, 'review/test.html', context=None)
        else:
            return render(request, 'review/404.html', context=None)
    except Exception,e:
        logging.error(e)
        return render(request, 'review/500.html',context=None)
