# incep_web

incep_web 是基于django框架、以及去哪网开源的inception审核组成，主要给用户提供一个web界面,方便日常sql审核的一个平台，平台包含预审核及审核功能。目前支持dml及create语法审核，后续也会进一步加入alter语法审核与线上执行。

## version
 	django 1.11.3
 	python 2.7.3
 	inception 2.1.23
 	incep_web 1.0
 
## 部署
  其中数据库配置依赖于inception的安装位置,用户密码一般是根据设置无需添加，端口可以随着安装时启动的端口设置，具体数据库配置如下
## mysql
### settings.py
```DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django 、
        'NAME': 'auto_database',     #主要数据库，存储审核的sql和数据库信息
        'USER': ',
        'PASSWORD': '',
        'HOST':'',
        'PORT':'3306',
    },
    'data_backup': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        'NAME': 'inception',     #存储备份数据库信息
        'USER': '',
        'PASSWORD': '',
        'HOST':'',
        'PORT':'3306',
    },
    'review': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        'NAME': '',   #执行sql审核后端审核服务，我的具体备份也放在inception同一台机器,如果不是同一台需添加新的备份机器
        'USER': 'root',
        'PASSWORD': '',
        'HOST':'',
        'PORT':'6669',
    }

}

DATABASE_ROUTERS = ['setting.databaseRouter.modelsRouter', 'setting.databaseRouter.ReportRouter','setting.databaseRouter.ExecuteRoutor']

### databaseRouter.py
  添加新的数据库时也需要在此文件添加具体权限信息
```

## 邮箱配置
	EMAIL_USE_TLS = False
	EMAIL_HOST = 'smtp.exmail.qq.com'
	EMAIL_PORT = 25
	EMAIL_HOST_USER = '446591512@qq.com'
	EMAIL_HOST_PASSWORD = '*****'
	DEFAULT_FROM_EMAIL = '446591512@qq.com'
## debug
	DEBUG = False
	
## amdin管理系统的配置
  管理系统入口就是django自带的后端管理,只需要在url后加admin：
  http://127.0.0.1:8080/admin
  
## 登录效果图
![](https://github.com/changyl/incep_web/blob/master/models/static/img/1.png)


## 仪表盘效果图
![](https://github.com/changyl/incep_web/blob/master/models/static/img/2.png)
![](https://github.com/changyl/incep_web/blob/master/models/static/img/3.png)
