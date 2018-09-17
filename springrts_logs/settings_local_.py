# -*- coding: utf-8 -*-

SECRET_KEY = 's3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3ts3cr3t'
DEBUG = False
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spring_logs',
        'USER': 'spring_logs',
        'PASSWORD': 's3cr3t',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}
TIME_ZONE = 'UTC'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
