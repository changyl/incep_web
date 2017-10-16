# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging,sys,MySQLdb
from django.db import connections

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='inceptionWeb.log',
                    filemode='a')





def Execute(user,password,host,port,dbname,content):
    """
    :param user:
    :param password:
    :param host:
    :param port:
    :param dbname:
    :param content:
    :return: sql
    :desc:拼接具体审核的sql格式
    :author:changyl
    """
    target_sql = '''/*--user={0};--password={1};--host={2};--execute=1;--enable-ignore-warnings;--port={3};*/'''.format(user,password,host,port)
    db_sql = '''use {0};'''.format(dbname)
    ddl_dml_sql = '''{0}''' .format(content)

    main_sql = '''{0}inception_magic_start;{1}{2} inception_magic_commit;'''.format(target_sql,db_sql,ddl_dml_sql)
    return main_sql


def fullExecute(user,password,host,port,dbname,content):
    """
    :param user:
    :param password:
    :param host:
    :param port:
    :param dbname:
    :param content:
    :return: sql
    :desc:拼接具体审核的sql格式
    :author:changyl
    """
    target_sql = '''/*--user={0};--password={1};--host={2};--execute=1;--port={3};*/'''.format(user,password,host,port)
    db_sql = '''use {0};'''.format(dbname)
    ddl_dml_sql = '''{0}''' .format(content)

    main_sql = '''{0}inception_magic_start;{1}{2} inception_magic_commit;'''.format(target_sql,db_sql,ddl_dml_sql)
    return main_sql


def preAuditExecute(user,password,host,port,dbname,content):
    """
    :param user:
    :param password:
    :param host:
    :param port:
    :param dbname:
    :param content:
    :return: sql
    :desc:拼接具体审核的sql格式
    :author:changyl
    """
    target_sql = '''/*--user={0};--password={1};--host={2};--enable-check;--port={3};*/'''.format(user,password,host,port)
    db_sql = '''use {0};'''.format(dbname)
    ddl_dml_sql = '''{0}''' .format(content)
    main_sql = '''{0}inception_magic_start;{1}{2} inception_magic_commit;'''.format(target_sql,db_sql,ddl_dml_sql)
    return main_sql

def inceptionQuery(main_sql):
    """
    :param main_sql:
    :return:返回审核结果
    :author:changyl
    """

    conn = MySQLdb.connect(host='172.16.16.20', user='root', passwd='', db='', port=6669)
    cur = conn.cursor()
    cur.execute(main_sql.encode('utf-8'))
    result = cur.fetchall()
    return result


def getUserInfo(username):
    '''
    :param username: cyl
    :return: 用户任务数、名称
    :desc:获取用户信息
    '''
    sql_sum = '''select count(*) from tb_review where (flag=0 or flag=1)   and  create_time >date_format(now(),'%Y-%m-%d 00:00:00')'''
    cursor = connections['default'].cursor()
    cursor.execute(sql_sum)
    sum_row = cursor.fetchone()
    dict = {}
    dict['name'] = username
    dict['taskCount'] = sum_row
    return dict

def getUserInfo_01(username,userid):
    '''
    :param username: cyl
    :return: 用户个体的任务数、名称
    :desc:获取用户信息
    '''
    sql_sum = '''select count(*) from tb_review where (flag=0 or flag=1)  and CREATOR={0} and  create_time >date_format(now(),'%Y-%m-%d 00:00:00')''' .format(userid)
    cursor = connections['default'].cursor()
    cursor.execute(sql_sum)
    sum_row = cursor.fetchone()
    dict = {}
    dict['name'] = username
    dict['taskCount'] = sum_row
    return dict

def getUserInfo_02(username,sql_id,userid):
    '''
    :param username:用户名称
    :param sql_id:sql id
    :return: 返回用户任务数、用户名称、sql审核内容
    '''
    sql_detail_info = '''select * from tb_review_detail where sql_id={0}'''.format(sql_id)
    cursor = connections['default'].cursor()
    cursor.execute(sql_detail_info)
    row = cursor.fetchall()
    sql_sum = '''select count(*) from tb_review where (flag=0 or flag=1) and creator={0} and create_time>date_format(now(),'%Y-%m-%d 00:00:00')''' .format(userid)
    cursor = connections['default'].cursor()
    cursor.execute(sql_sum)
    sum_row = cursor.fetchone()
    dict_report = {}
    dict_report['reportlist'] = row
    dict_report['taskCount'] = sum_row
    dict_report['name'] = username
    return  dict_report



def getUserInfoReport(username,userid):
    """
    :param username:
    :return: dict
    :author: changyl
    :desc: 返回用户信息,包括单选列表
    """
    sql_sum = '''select count(*) from tb_review where (flag=0 or flag=1) and creator={0} and create_time >date_format(now(),'%Y-%m-%d 00:00:00') ''' .format(userid)
    cursor = connections['default'].cursor()
    cursor.execute(sql_sum)
    sum_row = cursor.fetchone()
    sql_sum = '''select id,db_tag from tb_databases_config'''
    cursor = connections['default'].cursor()
    cursor.execute(sql_sum)
    datarows = cursor.fetchall()
    dict_report = {}
    dict_report['user'] = username
    dict_report['taskCount'] = sum_row
    dict_report['database'] = datarows
    return dict_report


def getUserInfoReport_02(userid,username):
    sql_sum = '''select count(*) from tb_review where flag=1 and create_time>date_format(now(),'%Y-%m-%d 00:00:00')'''
    cursor = connections['default'].cursor()
    cursor.execute(sql_sum)
    sum_row = cursor.fetchone()
    sql = '''SELECT 
                        a.id,
                        b.db_name,
                        a.content,
                        a.create_time,
                        a.flag,
                        a.review_time,
                        a.remarks,
                        a.remark_user
                    FROM
                        tb_review as a left join tb_databases_config as b
                        on a.database_id=b.id
                    WHERE
                        a.creator = {0} and a.create_time>date_format(now(),'%Y-%m-%d 00:00:00')'''.format(userid)
    cursor = connections['default'].cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    dict_report = {}
    dict_report['reportlist'] = row
    dict_report['user'] = username
    dict_report['taskCount'] = sum_row
    return dict_report



#获取用户类别
def getUserType(request):
    user_type = request.user.is_staff
    return user_type
