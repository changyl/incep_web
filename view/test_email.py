# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from __future__ import unicode_literals


send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['to@example.com'], fail_silently=False)