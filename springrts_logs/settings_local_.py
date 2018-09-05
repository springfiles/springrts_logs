# -*- coding: utf-8 -*-

SECRET_KEY = 's3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3t'
DEBUG = False
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spring_logs',
        'USER': 'spring_logs',
        'PASSWORD': 's3cr3t',
        'HOST': 'localhost',
        'PORT': '',
    },
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
}
TIME_ZONE = 'UTC'
