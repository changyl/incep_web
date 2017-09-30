# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import backup_done_list,backup_task_list
from models_inception import tb_review,tb_databases_config,tb_review_history
import base64
# Register your models here.


@admin.register(backup_done_list)
class donelistAdmin(admin.ModelAdmin):
    list_display = ('id','host_id','dbname','target_dir','source_dir','backup_size','tar_backup_size','start_time','create_time','is_complete','is_tar_complete')
    # fields = ()
    search_fields = ('dbname',)

    def  comp_boolean(self):
        return self.is_complete == 1
    comp_boolean.boolean=True

    def  backcomp_boolean(self):
        return self.is_tar_complete == 1
    backcomp_boolean.boolean=True



@admin.register(backup_task_list)
class tasklistAdmin(admin.ModelAdmin):
    list_display = ('host_id','host_ip','dbname','username','port','defaults_file','logdir','backup_path','level','flag','add_time')
    fields = ('host_id','host_ip','dbname','username','password','port','defaults_file','logdir','backup_path','level','flag',)
    # fields = ('dbname','username','password','port','defaults_file','datadir','backup_path','level','flag','add_time')
    search_fields = ('dbname',)

    def flag_boolean(self):
        print self.flag
        return self.flag == 1
    flag_boolean.boolean = True

    #active_status.short_description = 'Published recently?'
    def save_model(self, request, obj, form, change):
        if change:
            # obj.host_code = hashlib.md5(str(obj)).hexdigest()
            # obj.password = base64.encodestring(str(obj))
            #解密base64.decodestring
            obj.password = base64.encodestring(str(obj))
            # passwd = base64.decodestring(str(request.POST.get('password')))
        else:
            pass
        obj.password = base64.encodestring(str(request.POST.get('password')))
        obj.save()



    # def save_model2(self, request, obj, form, change):
    #     if change:
    #         obj.host_id = socket.ntohl(struct.unpack("I",socket.inet_aton(str(request.POST.get('password'))))[0])
    #     else:
    #         pass
    #     obj.host_id = socket.ntohl(struct.unpack("I",socket.inet_aton(str(request.POST.get('password'))))[0])
    #     obj.save()

@admin.register(tb_review)
class reviewAdmin(admin.ModelAdmin):
    list_display = ('id','database_id','content','creator','create_time','flag','review_id','review_time','remarks')
    # fields = ()
    search_fields = ('database_id',)

    def  flag_boolean(self):
        return self.flag == 1
    flag_boolean.boolean=True

@admin.register(tb_review_history)
class reviewHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'database_id', 'content', 'creator', 'create_time', 'flag', 'review_id', 'review_time', 'remarks')
    # fields = ()
    search_fields = ('database_id',)

@admin.register(tb_databases_config)
class dataConfigAdmin(admin.ModelAdmin):
    #list_display = ('id', 'host')
    list_display = ('id', 'host', 'user', 'passwd', 'port', 'db_name', 'create_time','creator','update_time','updator','flag','db_tag')
    fields = (
    'id', 'host', 'user', 'passwd', 'port', 'db_name', 'creator', 'update_time', 'updator', 'flag',
    'db_tag')
    search_fields = ('db_name',)

    def  backcomp_boolean(self):
        print self.flag
        return self.flag == 1
    backcomp_boolean.boolean=True
# admin.site.register(models.ba)
# admin.site.register()
# admin.site.register()
