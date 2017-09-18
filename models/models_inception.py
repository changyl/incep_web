# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

'''
定义inception相关模型
'''

class information_schema(models.Model):
    CATALOG_NAME    =   models.CharField(u'CATLOG名称',max_length=512)
    SCHEMA_NAME     =   models.CharField(u'CATLOG名称',max_length=64)
    DEFAULT_CHARACTER_SET_NAME  =  models.CharField(u'名称',max_length=32)
    DEFAULT_COLLATION_NAME  =  models.CharField(u'用户名称',max_length=32)
    SQL_PATH  =  models.CharField(u'用户名称',max_length=512)

    class Meta:
        verbose_name = '用户账户清零'
        verbose_name_plural = '用户账户清零'
        # db_table = "menus"  #重写数据表名称，覆盖类名
        # db_tablespace = "" 表空间名称

    def __unicode__(self):
        return self.SCHEMA_NAME



class tb_review(models.Model):
    id = models.AutoField(primary_key=True, max_length=11)
    database_id = models.IntegerField(u'数据库ID', )
    content = models.TextField(u'内容', )
    creator = models.IntegerField(u'创建人ID',)
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True )
    flag = models.IntegerField(u'是否通过', )
    review_id = models.IntegerField(u'审核人ID', )
    review_time = models.DateTimeField(u'审核通过时间',)
    remarks = models.CharField(u'备注信息',max_length=512)
    remark_user = models.CharField(u'用户备注信息',max_length=512)
    class Meta:
        verbose_name = '审核表'
        verbose_name_plural = '审核表'
        db_table = "tb_review"  #重写数据表名称，覆盖类名
        # db_tablespace = "" 表空间名称

    def __unicode__(self):
        return self.database_id

class tb_review_history(models.Model):
    id    =   models.AutoField(primary_key=True,max_length=11)
    database_id     =   models.IntegerField(u'数据库ID',)
    content  =  models.TextField(u'内容',)
    creator  =  models.IntegerField(u'创建人ID',)
    create_time  =  models.DateTimeField(u'创建时间',)
    flag    =   models.IntegerField(u'是否通过',)
    review_id   =   models.IntegerField(u'审核人ID',)
    review_time =   models.DateTimeField(u'审核通过时间',)
    remarks = models.CharField(u'审核信息',max_length=512)
    class Meta:
        verbose_name = '审核历史表'
        verbose_name_plural = '审核历史表'
        db_table = "tb_review_history"  #重写数据表名称，覆盖类名
        # db_tablespace = "" 表空间名称

    def __unicode__(self):
        return self.database_id

class tb_databases_config(models.Model):
    auto_id = models.AutoField(primary_key=True)
    id    =   models.IntegerField(u'数据库ID',)
    host     =   models.CharField(u'IP',max_length=45)
    user  =  models.CharField(u'用户名称',max_length=45)
    passwd  =  models.CharField(u'密码',max_length=45)
    port  =  models.IntegerField(u'端口',)
    db_name = models.CharField(u'数据库名称',max_length=45)
    create_time =   models.DateTimeField(u'创建时间',auto_now_add=True )
    creator =   models.IntegerField(u'创建人ID',)
    update_time =   models.DateTimeField(u'更新时间',)
    updator =   models.IntegerField(u'更新人ID',)
    flag    =   models.IntegerField(u'是否启用',)
    db_tag = models.CharField(u'数据库标签',max_length=45)

    class Meta:
        verbose_name = '数据库配置'
        verbose_name_plural = '数据库配置'
        db_table = "tb_databases_config"  #重写数据表名称，覆盖类名
        # db_tablespace = "" 表空间名称

    def __unicode__(self):
        return self.db_name



