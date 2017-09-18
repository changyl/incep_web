# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging,sys,MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='inceptionWeb.log',
                    filemode='a')


def auditActive(user,password,host,port,dbname,content):
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
    logging.info('test')
    return result
