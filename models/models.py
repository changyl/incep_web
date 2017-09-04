# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.



class backup_done_list(models.Model):
    id = models.AutoField(primary_key=True,max_length=11)
    host_id = models.IntegerField(u'主机ID',)
    dbname = models.CharField(u'数据库名称',max_length=20)
    target_dir = models.CharField(u'目标目录',max_length=512)
    source_dir = models.CharField(u'源目录',max_length=512)
    backup_size = models.DecimalField(u'原始备份大小(G)',decimal_places=4,max_digits=10)
    tar_backup_size = models.DecimalField(u'压缩备份大小(G)',decimal_places=4,max_digits=10)
    start_time = models.DateTimeField(u'开始时间',auto_now_add=True)
    create_time = models.DateTimeField(u'结束时间',auto_now_add=True)
    is_complete = models.BooleanField(u'备份是否完成',)
    is_tar_complete = models.BooleanField(u'压缩是否成功',)
    class Meta:
        verbose_name = '备份'
        verbose_name_plural = '备份'
        db_table = "backup_done_list"  #重写数据表名称，覆盖类名
        #db_tablespace = "" 表空间名称

    def __unicode__(self):
        return self.dbname





class backup_task_list(models.Model):
    start = 1
    nostart = 0
    YEAR_IN_SCHOOL_CHOICES = (
        (start, '开启'),
        (nostart, '关闭'),
    )
    id = models.AutoField(primary_key=True,max_length=11)
    host_id = models.CharField(u'主机ID',max_length=20)
    host_ip = models.CharField(u'远程主机IP',max_length=20)
    dbname = models.CharField(u'数据库名称',max_length=40)
    username = models.CharField(u'用户名称',max_length=30)
    password = models.CharField(u'用户密码',max_length=50)
    port = models.IntegerField(u'端口')
    defaults_file = models.CharField(u'默认文件',max_length=45)
    logdir = models.CharField(u'日志目录',max_length=512)
    backup_path = models.CharField(u'备份路径',max_length=512)
    level = models.IntegerField(u'备份级别',)
    # flag = models.BooleanField(u'备份是否开启',choices=YEAR_IN_SCHOOL_CHOICES,default=nostart)
    flag = models.BooleanField(u'备份是否开启',)
    add_time = models.DateTimeField(u'添加时间',auto_now_add=True)

    def __unicode__(self):
        return u'%s,%s' % (self.password,self.host_id)


    class Meta:
        verbose_name = '任务'
        verbose_name_plural = "任务"
        db_table = "backup_task_list"









