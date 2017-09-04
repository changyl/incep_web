# incep_web

incep_web 是基于django框架、以及inception后端审核组成，主要给用户提供一个web界面去操作、展示sql审核的一个平台。

# version
 	django 1.11.3
 	python 2.7.3
 	inception 2.1.23
 	incep_web 1.0
 
# 部署
	其中数据库配置依赖于inception的安装位置，具体配置：
## mysql
```DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        'NAME': 'auto_database',
        'USER': 'cyl',
        'PASSWORD': 'cyl_young',
        'HOST':'172.16.16.29',
        'PORT':'3306',
    },
    'data_backup': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        'NAME': 'inception',
        'USER': 'incep_stat',
        'PASSWORD': 'cyl_soyoung',
        'HOST':'172.16.16.20',
        'PORT':'3306',
    },
    'review': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        #'NAME': '',
        'USER': 'root',
        'PASSWORD': '',
        'HOST':'172.16.16.20',
        'PORT':'6669',
    }

}
```

