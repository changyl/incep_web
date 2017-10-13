# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse as write
from django.shortcuts import render
from django.db import connections
from django.contrib.auth.views import login_required
import collections,json,datetime,sys,logging
from baseTools import getUserInfo

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='incption_web.log',
                    filemode='a')

