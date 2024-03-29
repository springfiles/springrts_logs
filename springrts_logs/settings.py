# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'springrts_logs',
    'rest_framework',
    'drf_yasg',
    'modernrpc',
    'rest_hooks',
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

ROOT_URLCONF = 'springrts_logs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'springrts_logs.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': (
        'springrts_logs.rpc_methods.JsonTcpAnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '200/hour',
    },
}
MODERNRPC_HANDLERS = ['modernrpc.handlers.JSONRPCHandler']
MODERNRPC_METHODS_MODULES = [
    'springrts_logs.rpc_methods',
]
MODERNRPC_DOC_FORMAT = 'rst'

LOGFILE_TAG_TO_EVENT = {
    'spring-launcher': ('logfile.added.spring_launcher', 'springrts_logs.Logfile.created_spring_launcher+', ),
}
# HOOK_EVENTS = {
#     # 'any.event.name': 'App.Model.Action' (created/updated/deleted)
#     'logfile.added.spring_launcher': 'springrts_logs.Logfile.created_spring_launcher+',
# }
HOOK_EVENTS = dict(LOGFILE_TAG_TO_EVENT.values())

# import default site specific settings
from .settings_local_ import *
# import custom site specific settings
try:
    from .settings_local import *
except ImportError as exc:
    print('ImportException: {}\nCopy local_settings_.py to local_settings.py and adapt to your environment.'.format(exc))
    raise
