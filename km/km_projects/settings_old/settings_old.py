# -*- coding: utf-8 -*-
# Django settings
# TODO: уйти от конфигурационных файлов БД cnf, перенеся их в settings_local

import os

from django.core.exceptions import ImproperlyConfigured

PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))

DEBUG = False

# дирректория сохранения логов
LOGS_DIR = os.path.join(PROJECT_PATH, 'logs')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# При внесении изменений смотреть ниже по коду на секцию
# которая работает при включенном дебагинге
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, 'templates')
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'catalog.context_processors.template_for_autofill_catalog_item',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader'
            ]
        },
    },
]

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'gunicorn',
    'mptt',
    'tinymce',
    'filebrowser',
    'jsonfield',
    'genericadmin',

    'catalog',
    'ones',
    'cards',
    'configurator',
    'configurator.analitics',
    'online_shopping',
    'profiles',
    'snr',
    'sales_base_models',
    'broker'
)
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.7.77:6379/15",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    },
    'filebased': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(PROJECT_PATH, 'cache'),
    },
}

# Admintools

ADMIN_TOOLS_MENU = 'menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

DATABASE_ROUTERS = ['routers.Routers', 'sales_base_models.routers.Router']

# Настройки celery
CELERY_TASK_RESULT_EXPIRES = 300    # 5 минут
CELERY_IGNORE_RESULT = True
CELERY_ACKS_LATE = True

from kombu import Exchange, Queue

default_exchange = Exchange('default')
CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('system', default_exchange, routing_key='system'),
    Queue('description', default_exchange, routing_key='description'),
    Queue('image_prepare', default_exchange, routing_key='image_prepare'),
)

CELERY_DEFAULT_QUEUE = 'default'

# Tinymce

TINYMCE_DEFAULT_CONFIG = {
    # расширенный функционал
    'theme': "advanced",
    'plugins': "table,searchreplace,style,paste,advhr,advimage,advlink",
    'theme_advanced_buttons1': "bold,italic,underline,strikethrough,|"
                               ",justifyleft,justifycenter,justifyright,"
                               "justifyfull,styleprops,formatselect,"
                               "fontselect,fontsizeselect,|,forecolor,"
                               "backcolor,|,charmap,advhr",
    'theme_advanced_buttons2': "cut,copy,paste,pastetext,pasteword,|,bullist,"
                               "numlist,|,outdent,indent,blockquote,|,"
                               "undo,redo,|,link,unlink,anchor,image,"
                               "cleanup,help,code,|,hr,removeformat,"
                               "visualaid,|,sub,sup",
    'theme_advanced_buttons3': "",
    'theme_advanced_toolbar_location': "top",
    # абсолютные адреса у изображений
    'convert_urls': 1,
    'relative_urls': 0,
    'remove_script_host': 1,
    # высота контрола
    'height': '400',
    # ширина контрола
}

# кол-во кодов, передаваемых для запуска 1-го таска
# для обновлении слепка и выгрузки картинок на CDN, None-> всё в одном таске
COUNT_ITERATED = 100

# Время жизни кэша для хранения информации о "пачках подтверждения" карточек
# товара (24 часа)
UPDATE_DESCRIPTION_CACHE_TIMEOUT = 60 * 60 * 24

# Конфигурация filebrowser
FILEBROWSER_DIRECTORY = 'filebrowser_uploads/'
FILEBROWSER_DEFAULT_PERMISSIONS = None

DATABASES = {
    # '1c_8_raw': {}
}

SITE_PRODUCTS_REPORT_EMAILS = []

# список получателей рассылки о наличии 404 переходов с внешки
URL_404_WARNING_NOTIFICATION_GROUP = []

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp1.km-union.ru'
EMAIL_DEFAULT_FROM = 'admin@magic.km-union.ru'

# TODO: При добавлении нового типа магазина, не забудь добавить права в
# модель catalog.models.Catalog
# также имена используются в именах сигналах для брокера (таск sync_shop),
# изменить на стороне проекта broker
ONLINE_SHOPPING_TYPE_CHOICES = (
    (u'korallmicro', u'Интернет-магазин "КораллМикро"'),
    (u'istore', u'Интернет-магазин "Офисный Мир КМ"'),
    (u'snr_new', u'Интернет-магазин "SNR"'),
    (u'boxit', u'Электронный каталог "Boxit.pro"'),
)
# в админке, для перехода с отзыва о товаре на сайт с которого он был сделан
SEARCH_URL_MASKS = {
    u'korallmicro': u'http://www.korallmicro.ru/products/search/?token={}',
    u'istore': u'http://офисныймиркм.рф/search/?token={}',
    u'snr_new': u'https://snr.ru/search/?token={}',
}
DEFAULT_SHOPPING_TYPE = 'korallmicro'

# Разрешенные типы магазинов, используемые в логике формирования шаблонов
ENABLE_ONLINE_SHOPPING_TYPE_CHOICES = (
    (u'korallmicro', u'Интернет-магазин "КораллМикро"'),
    (u'snr_new', u'Интернет-магазин "SNR"'),
)

# отображение на сайте названия фильтра для выгодных предложений
OFFER_FILTER_NAME = u'Акционные предложения'

# stfp connections to our hostings
SFTP_CONNECTIONS = {
    # авторизация по ключу
    'cdn': {
        'host': '10.10.100.5',
        'port': 22,
        'username': 'devel',
        'password': ''
    },
}

CHANGE_LOGS_DIR = os.path.join(PROJECT_PATH, 'change_log')

# уровень сжатия (используется в moduels/cards/tasks.py, prepare_preview_for_watermark)
COMPRESSION_QUALITY = 90

# Списаок IP адресов, с которых разрешено взаимодействие с API (Не уверен что
# это имеет смысл)
ALLOW_IPS_FOR_API = []

DEFAULT_FILE_STORAGE = 'storage.SFTPStorage'

# Критическая группа для информирования
CRITICAL_ERROR_EMAIL_GROUPS = {
    'phones': [79043444247],
    'emails': [
        'alexandr_angilenko@km-union.ru'
    ]
}

BROKER_PREFIX_SOURCE = "Magic"

# Набор разделителей для транслита по типу магазина
TRANSLIT_DELIMETERS = {
    'snr_new': '-',
    'default': '_'
}

# соответствие типа магазина и моделей
# SHOPPING_TYPE: SITE_MODELS
SHOPPING_TYPES_MODELS = {
    'snr_new': 'sales_base_models.models',
    'korallmicro': 'korallmicro.models',
}

# crontab
from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {

    #####################
    ## for configurator #
    #####################

    'configurator_analitics': {
    'task': 'configurator_analitics',
        'schedule': crontab(day_of_month='10', minute='0', hour='8'),
        'options': {
            'routing_key': 'default'
        }
    },

    #####################
    ##### for magic #####
    #####################

    # синхронизация производителей из справочника в 1С
    'task_sync_brands': {
        'task': 'sync_brands',
        'schedule': crontab(minute='5', hour='7'),
        'options': {
            'routing_key': 'system'
        }
    },

    # проверка на актуальность, соответствие значения производитель и вид-подвид
    # в карточках товара и значений в 1С
    'task_sync_brands_kinds_in_actual_cards': {
        'task': 'sync_brands_kinds_in_actual_cards',
        'schedule': crontab(minute='10', hour='7'),
        'options': {
            'routing_key': 'system'
        }
    },

    # синхронизация баллов для бонус клуба розницы "Офисный мир КМ"
    'task_sync_bonusclub': {
        'task': 'sync_bonusclub',
        'schedule': crontab(minute='0', hour='8-20'),
        'options': {
            'routing_key': 'system'
        }
    },

    # рассылка сообщений об окончании выгодных предложений
    'task_offers_email_report': {
        'task': 'offers_email_report',
        'schedule': crontab(minute='30', hour='8-17'),
        'options': {
            'routing_key': 'system'
        }
    },

    # сброс признака "Опубликовано" для элементов карусель
    'task_unpublicate_carousel_items': {
        'task': 'unpublicate_carousel_items',
        'schedule': crontab(minute='0', hour='8'),
        'options': {
            'routing_key': 'system'
        }
    },

    # подготовка кеша с описаниями для Яндекс.Маркета
    'task_create_and_remember_yandex_market_description': {
        'task': 'create_and_remember_yandex_market_description',
        'schedule': crontab(minute='0', hour='8'),
        'options': {
            'routing_key': 'description'
        }
    },

    #####################
    ##### for sites #####
    #####################

    # при изменении времени синхронизаций korallmicro, istore, snr
    # изменять задачу по крону ротации индексов для sphinx (7.23)

    # сигнал окончания частичной синхронизации от 1С
    # TODO: будет посылаться от 1С
    'simple_ones_sync_morning': {
        'task': 'simple_ones_sync_send_signal',
        'schedule': crontab(minute='*/15', hour='0-7'),
        'options': {
            'routing_key': 'system'
        }
    },

    # сигнал окончания полной синхронизации от 1С
    # TODO: будет посылаться от 1С
    'task_sync_db': {
        'task': 'full_ones_sync_send_signal',
        'schedule': crontab(minute='6,36', hour='8-20'),
        'options': {
            'routing_key': 'system'
        }
    },

    # TODO: будет посылаться от 1С
    'simple_ones_sync': {
        'task': 'simple_ones_sync_send_signal',
        'schedule': crontab(minute='20,50', hour='8-20'),
        'options': {
            'routing_key': 'system'
        }
    },

    # TODO: будет посылаться от 1С
    'simple_ones_sync_evening': {
        'task': 'simple_ones_sync_send_signal',
        'schedule': crontab(minute='*/15', hour='21-23'),
        'options': {
            'routing_key': 'system'
        }
    },

    # синхронизация фильтров для сайта кораллмикро
    'task_sync_filter_korallmicro': {
        'task': 'sync_filter_korallmicro',
        'schedule': crontab(minute='0', hour='8-20'),
        'options': {
            'routing_key': 'system'
        }
    },

    # ежемесячный отчет для Саши Глубокова для korallmicro
    'send_report_korallmicro': {
        'task': 'send_report_korallmicro',
        'schedule': crontab(day_of_month=1, minute=0, hour=1),
    },

    # ежемесячный отчет для Саши Глубокова для SNR
    'send_report_snr': {
        'task': 'send_report_snr',
        'schedule': crontab(day_of_month=1, minute=0, hour=1),
        'kwargs': {
            # для всех поддоменов - [], пример конкректных - ['www', 'anapa']
            "subdomains": [],
        }
    },
}


from settings_local import *

# глобальная и групповая наценка для синхронизации с istore
if not ADDITIONAL_COST_FOR_ISTORE:
    raise ImproperlyConfigured(
        'ADDITIONAL_COST_FOR_ISTORE for sync_catalogs_and_products must be set'
    )


if not DEBUG and not ALLOW_IPS_FOR_API:
    raise ImproperlyConfigured("ALLOW_IPS_FOR_API don't configure")

DATABASES.update(LOCAL_DATABASES)

SFTP_CONNECTIONS['istore'] = {
    'path': PATH_TO_ISTORE,
    'catalog': os.path.join(PATH_TO_ISTORE, 'catalog/'),
    'product': os.path.join(PATH_TO_ISTORE, 'product/')
}
SFTP_CONNECTIONS['istore'].update(SFTP_CONNECTIONS['cdn'])

SFTP_CONNECTIONS['korallmicro'] = {
    'path': PATH_TO_KORALLMICRO,
    'catalog': os.path.join(PATH_TO_KORALLMICRO, 'catalog/'),
    'product': os.path.join(PATH_TO_KORALLMICRO, 'product/'),
    'article': os.path.join(PATH_TO_KORALLMICRO, 'article/'),
    'carousel': os.path.join(PATH_TO_KORALLMICRO, 'carousel/'),
    'seo': os.path.join(PATH_TO_KORALLMICRO, 'seoblock/'),
    'offer': os.path.join(PATH_TO_KORALLMICRO, 'offer/'),
    'product_tag': os.path.join(PATH_TO_KORALLMICRO, 'product_tag/'),
}
SFTP_CONNECTIONS['korallmicro'].update(SFTP_CONNECTIONS['cdn'])

SFTP_CONNECTIONS['snr_new'] = {
    'path': PATH_TO_SNR,
    'catalog': os.path.join(PATH_TO_SNR, 'catalog/'),
    'product': os.path.join(PATH_TO_SNR, 'product/'),
    'article': os.path.join(PATH_TO_SNR, 'article/'),
    'carousel': os.path.join(PATH_TO_SNR, 'carousel/'),
    'seo': os.path.join(PATH_TO_SNR, 'seoblock/'),
    'offer': os.path.join(PATH_TO_SNR, 'offer/'),
    'product_tag': os.path.join(PATH_TO_SNR, 'product_tag/'),
}
SFTP_CONNECTIONS['snr_new'].update(SFTP_CONNECTIONS['cdn'])

# переопределение Storage для хранения медийки на cdn
SFTP_CONNECTIONS['storage'] = {
    'path': PATH_TO_STORAGE,
    'media_url': 'http://cdn2.km-union.ru/magic/'
}
SFTP_CONNECTIONS['storage'].update(SFTP_CONNECTIONS['cdn'])

SFTP_STORAGE_CONFIG = SFTP_CONNECTIONS['storage']


if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    DISABLE_PANELS = []
    DEBUG_TOOLBAR_PATCH_SETTINGS = True

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': lambda x: True
    }

    # additional modules for development
    INSTALLED_APPS += (
        'debug_toolbar',
    )

    # Отключаем кеширование и добавляем toolbar при дебагинге
    MIDDLEWARE_CLASSES = (
        ('debug_toolbar.middleware.DebugToolbarMiddleware',) +
        MIDDLEWARE_CLASSES[1:-1]
    )

ADDITIONAL_HANDLERS ={
    'sftp_pool_connection_log': {
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': os.path.join(LOGS_DIR, 'sftp.log'),
        'maxBytes': 50000,
        'backupCount': 2,
        'encoding': 'UTF-8',
    },
}

ADDITIONAL_LOGGERS ={
    'sftp': {
        'handlers': ['sftp_pool_connection_log'],
        'level': 'INFO',
        'propagate': False
    }
}

LOGGING['handlers'].update(ADDITIONAL_HANDLERS)
LOGGING['loggers'].update(ADDITIONAL_LOGGERS)
