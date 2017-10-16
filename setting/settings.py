# -*- coding: utf-8 -*-

"""
Django settings for backup project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os,databaseRouter

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4_o(_78a*2ln8mhmpm^ju(o0dgt0^g-ix00n#j@d%b&9twc-5o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'models',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setting.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

#mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        'NAME': 'auto_database',
        'USER': 'inception',
        'PASSWORD': '',
        'HOST':'',
        'PORT':'3306',
    },
    'data_backup': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        'NAME': 'inception',
        'USER': 'incep_stat',
        'PASSWORD': '',
        'HOST':'',
        'PORT':'3306',
    },
    'review': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        #'NAME': '',
        'USER': 'root',
        'PASSWORD': '',
        'HOST':'',
        'PORT':'6669',
    }

}





DATABASE_ROUTERS = ['setting.databaseRouter.modelsRouter', 'setting.databaseRouter.ReportRouter','setting.databaseRouter.ExecuteRoutor']
# DATABASE_APPS_MAPPING = {
#     # example:
#     #'app_name':'database_name',
#     'backup': 'data_backup',
#     # 'models': 'review',
# }



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en_CH'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
#登录url设置
LOGIN_URL = 'user/v1.0/account/login/'

STATIC_URL = '/models/static/'
STATIC_ROOT = '/home/'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
# STATIC_ROOT = (
#     os.path.join(BASE_DIR, 'static').replace('\\', '/')
#
# )

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''


#Django Suit配置示例
SUIT_CONFIG  =  {
    #header
    'ADMIN_NAME': '数据库管理系统',
    'HEADER_DATE_FORMAT':'l,F Y',
    'HEADER_TIME_FORMAT':'h:i',

    #forms
    'SHOW_REQUIRED_ASTERISK':True, #Default True
    'CONFIRM_UNSAVED_CHANGES':True, #Default True

    # menu
    # 'SEARCH_URL':'/admin/',
    # 'MENU_ICONS':{
    # 'sites':'icon-leaf',
    # 'auth':'icon-lock',
    # },
    'MENU_OPEN_FIRST_CHILD':True,#Default True
    #'MENU_EXCLUDE':('auth.group',),
    'MENU':(
    'site',
    {'app':'models','label':u'任务管理','icon':'icon-tasks','models': ({'model': 'backup_task_list', 'label': '任务列表'}, )},
    {'app':'models','label':u'备份管理','icon':'icon-th-list','models': ({'model': 'backup_done_list', 'label': '备份列表'},)},
    {'app':'models','label':u'数据库配置管理','icon':'icon-cog','models': ({'model': 'tb_databases_config', 'label': '数据库配置列表'}, )},
    {'app':'models','label':u'SQL审核管理','icon':'icon-edit','models': ({'model': 'tb_review', 'label': 'SQL审核列表'},)},
    ),

    #miscu
    'LIST_PER_PAGE':10
}

