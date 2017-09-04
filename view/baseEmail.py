# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.mail import send_mail

import logging,sys

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='data_manage.log',
                    filemode='a')




class sendEmail:
    '''初始化email参数'''
    def __init__(self,title=None,message=None,from_email=None,to_email=None):
        self.em_titile = title
        self.em_message = message
        self.em_f_email = from_email
        self.em_t_email = to_email

    def send(self,):
        '''发送具体邮件'''
        send_mail(self.em_titile,self.em_message,self.em_f_email,['%s' % self.em_t_email],fail_silently=True)


