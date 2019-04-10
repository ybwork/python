# -*- coding: utf-8 -*-

from celery.schedules import crontab
from datetime import timedelta
# Определяет параметры работы пакета esb_events
from kombu.common import Exchange, Queue

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

LOCAL_DATABASES = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dealer_price',
        'PASSWORD': 'dealer_price',
        'USER': 'dealer_price',
        'HOST': 'dealer-price-db.km-union.ru'
    },
    'unique_price': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'dealer-price-db.km-union.ru',
        'NAME': 'uniq_price',
        'USER': 'dealer_price',
        'PASSWORD': 'dealer_price',
    },
    'sales_base_models': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '192.168.7.9',
        'PORT': '5432',
        'NAME': 'korallmicro',
        'PASSWORD': 'korallmicro',
        'USER': 'korallmicro',
    },
    'events': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '192.168.7.9',
        'PORT': '5432',
        'NAME': 'order',
        'PASSWORD': 'korallmicro',
        'USER': 'korallmicro',
    },
    'magic': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'new-mysql.km-union.ru',
        'NAME': 'magic',
        'USER': 'magic',
        'PASSWORD': 'megamagic',
    },
    'one_c_raw': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'new-mysql.km-union.ru',
        'NAME': '1C_8_RAW',
        'USER': 'ones',
        'PASSWORD': 'oneskm',
    },
    'kmclient': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'km-client-db.km-union.ru',
        'NAME': 'kmclient8',
        'USER': 'kmclient8',
        'PASSWORD': 'bold4fx',
    },
    'kmclient8local': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'new-mysql.km-union.ru',
        'NAME': 'kmclient_web_data',
        'USER': 'kmclient_web',
        'PASSWORD': '4S)Fkzv]f<)6N0q;',
    },
    'linked': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '192.168.7.74',
        'NAME': 'grabber_v3',
        'USER': 'grabbers',
        'PASSWORD': 'grabbers',
    },
}

ALLOWED_HOSTS = []

SECRET_KEY = '(h7lvlk9p@qd$#+-srxyias9+cw3tt=^x_opehc+7ck5m!g0b@'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BROKER_URL = [
    # Важно, чтобы на локальной машине было подключение к локальному rabbit-у,
    # чтобы не отправить задачи в боевой
    "amqp://guest:guest@localhost:5672/dp"
]
BROKER_TARGET_URL = [
    # Важно, чтобы на локальной машине было подключение к локальному rabbit-у,
    # чтобы не отправить задачи в боевой
    "amqp://guest:guest@localhost:5672/broker"
]

CELERY_TASK_RESULT_EXPIRES = 60 * 20

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp3.km-union.ru'
SERVER_EMAIL = 'local_dp_error@km-union.ru'

REMAINS_REMOVE_FILE_AFTER_IMPORT = False

TEST_USER_UUID = '45ea43c7-0be6-11e4-80b8-6805ca183101'
TEST_USER_REMAINS_FROM_UUID = '80126387-b1f8-11e2-93f1-002655df3ac1'
USER_REMAINS_OVERRIDE = {
    'ee491f5a-5a8e-11e4-80c9-001b21d8d330':
        '86dc1126-b1f8-11e2-93f1-002655df3ac1'
}

LAST_SYNCHRONIZATION_MAX_EXECUTION_TIME = 135

LOCAL_TEMPLATE_CONTEXT_PROCESSORS = ()

LAST_SYNCHRONIZATION_EMAIL_NOTIFICATION_GROUP = ['kaduk_ia@km-union.ru']

YA_AUDIENCE_REPORT_EMAILS = ['kaduk_ia@km-union.ru']

CHECK_SYNC_PRICE_EMAIL_GROUP = ['kaduk_ia@km-union.ru']

NOTIFY_KM_ORDERS_DELAYED_EMAILS = []

DELAYED_ORDER_PROCESSING_NOTIFICATION_GROUP = ['kaduk_ia@km-union.ru']

ORDER_WITH_NOTICE_NOTIFICATION_GROUP = ['kaduk_ia@km-union.ru']

# Сайты по которым не нужно отсылать уведомления об ошибках лицам в
# DELAYED_ORDER_PROCESSING_NOTIFICATION_GROUP
DEALER_SITE_IDS_FOR_NOT_NOTIFY_ORDER_ERRORS = [
    # www.korallmicro.ru
    1,
    # krasnodar.korallmicro.ru
    37,
    # taganrog.korallmicro.ru
    28,
    # shakhty.korallmicro.ru
    14
]

ONEC7_FILES_PATH = '/home/web/www/dealer_price/csv/ones7'

# группа емайлов сектора 1С
GET_REMAINS_ERROR_NOTIFICATION_GROUP = ['nikita_korotaev@km-union.ru']

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CREATE_ORDER_RATE = '100/m'

SMS_BLACK_LIST = [u'71111111111', u'79999999999', u'78888888888',
                  u'7__________', u'70000000000', u'70000000000']

# Наши сайты, которые не используют интерфейс для распределения количества в
# пункте заказа по складам
SITES_NOT_DISTRIBUTION_ORDERS_MANUAL = [
    # 1
    'www.korallmicro.ru',
    # 37
    'krasnodar.korallmicro.ru'
]

DEFAULT_SHOPPING_TYPE = ''

DEFAULT_PRICE_TYPE = ''

DEFAULT_SHOPPING_TYPES = ['korallmicro']

exchange = Exchange('magic', 'fanout')

ESB_EVENTS_CONFIG = {
    'BROKER_URL': [
        'amqp://web:web_password@192.168.7.76:5672/esb_events',
        'amqp://web:web_password@192.168.7.77:5672/esb_events'
    ],
    'CELERY_QUEUES': (
        Queue('dp', exchange),
    ),
    'CELERY_DEFAULT_QUEUE': 'dp'
}

ESB_EVENTS_BROKER_URL = [
    'amqp://web:web_password@192.168.7.76:5672/esb_events',
    'amqp://web:web_password@192.168.7.77:5672/esb_events'
]

# Кому отправлять сообшения при несоответствии суммы оплаты и суммы заказа
PAYMENT_SEND_ERROR_EMAILS = ['kaduk_ia@km-union.ru']

INFO_MAX_RETRIES_SMS_SEND_EMAILS = ['kaduk_ia@km-union.ru']

DEVIANT_EMAILS_LIST_BY_DEFAULT = ['kaduk_ia@km-union.ru']

DEVIANT_EXCLUDE_DOMAIN = ['kaduk_ia@km-union.ru']

# для DEALERS_DEVIANT_PRICE_OPTIONS
rostov_subdomain_deviant_options = {
    'delta_percent': 1,
    'hide_action_product': True,
    'emails_list': ['kaduk_ia@km-union.ru'],
    'price_uuid': 'aa1aecce-b99d-4f9b-ae1e-b10e8bd5c555',
}

# Словарь с параметрами задания условий применения логики "Девиантные цены"
DEALERS_DEVIANT_PRICE_OPTIONS = {
    'www.korallmicro.ru': rostov_subdomain_deviant_options,
    'krasnodar.korallmicro.ru': rostov_subdomain_deviant_options,
    'samara.korallmicro.ru': rostov_subdomain_deviant_options,
    'taganrog.korallmicro.ru': rostov_subdomain_deviant_options,
    'volgodonsk.korallmicro.ru': rostov_subdomain_deviant_options,
}

KM_FILIALS = {
    # uuid соглашения
    # Пример:
    # '7b5b7e4f-70b5-11e4-80ce-001b21d8d330': {
    #    # uuid цены
    #    'price': '7b5b7e4f-70b5-11e4-80ce-001b21d8d330'
    # },
}

# или 'snr_new'
DEFAULT_SHOPPING_TYPE = 'korallmicro'

# критерий отбора event-ов и заказов конкретного сайта
DOMAIN_FOR_EVENT_MODULE = 'korallmicro.ru'

TYPE_TEMPL_FORM = 'korallmicro'

DEFAULT_PROFILE_DEALER_UUID = 'cd5cc581-70b4-11e4-80ce-001b21d8d330'

DEFAULT_PROFILE_AGREEMENT_UUID = '7b5b7e4f-70b5-11e4-80ce-001b21d8d330'

ONLINE_PAYMENT_ERROR_NOTIFICATION_GROUP = ['kaduk_ia@km-union.ru']

SHOP_PASSWORD = {
    148566: 'KorallMicroForever',
    514826: 'KorallMicroForever',
}

# дефолтные параметры подключения к редису для семафора
SEMAPHORE_REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 3
}

ATOMPARK_COURCE = '1.5'

ONES_ERROR_NOTIFICATION_GROUP = ['lopatkin_de@km-union.ru']

# url основа которого будет браться для формирования ссылки
# для публичного доступа
PUBLIC_URL = ''

# Кого уведомлять о некорректных связках каталога и групп money care
MANAGER_MONEY_CARE = []

# Настройки сбора статистики на проекте
STATSY_VIEW_PERMISSION = 'statsy.stats_view'
STATSY_CACHE_NAME = 'statsy'

LOCAL_CELERYBEAT_SCHEDULE = {
    'sync_specific_gravities': {
        # пересчитывает удельный вес для всех элементов
        'task': 'sync_specific_gravities',
        'schedule': crontab(hour=5, minute=0),
    },
    'fill_intermediate_values': {
        # формируем промежуточные значения для активных ТК
        'task': 'fill_intermediate_values',
        'schedule': crontab(hour=5, minute=30),
    },
    # 'recompute_charges': {
    #     # устанавливает наценку на позиции для всех профилей
    #     'task': 'recompute_all_charges',
    #     'schedule': crontab(hour=7, minute=0),
    # },
    'update_orders': {
        'task': 'check_and_update_km_orders',
        'schedule': timedelta(minutes=1),
        'relative': True
    },
    'check_delivery_states': {
        'task': 'check_delivery_states',
        'schedule': crontab(hour=9, minute=0),
    },
    'restore_link': {
        'task': 'restore_link',
        'schedule': crontab(hour=9, minute=0),
    },
    #'check_payed_yandex': {
    #    # проверка писем от ресурса Яндекс.Деньги (акт сверки)
    #    'task': 'check_payed_yandex_email',
    #    'schedule': timedelta(hours=1),
    #    'relative': True
    #},
    'check_unsended_orders': {
        'task': 'check_unsended_orders',
        'schedule': timedelta(minutes=60),
        'relative': True
    },
    'celery.backend_cleanup': {
        'task': 'celery.task.backend_cleanup',
        'schedule': timedelta(minutes=60),
        'relative': True,
    },
    'check_synchronizations': {
        # проверка успешности синхронизаций
        'task': 'check_synchronizations',
        'args': (['joint'],),
        'schedule': timedelta(minutes=5),
    },
    'check_last_synchronizations': {
        # проверка успешности синхронизаций
        'task': 'check_last_synchronizations',
        'args': (['joint'],),
        'schedule': crontab(hour=9, minute=0),
    },
    # 'clear_uploaded_profile_log': {
    #     # Чистка лога выгруженных профилей
    #     'task': 'clear_uploaded_profile_log',
    #     'schedule': crontab(0, 0, day_of_month=1),
    # },
}

SENDER_EMAIL_ADDRESS = 'admin@km-union.ru'

# url на moneyCare
MONEY_CARE_URL = 'https://mc1.moneycare.su'

# логин пароль для авторизации в MoneyCare
AUTH_MONEY_CARE = {
    'login': 'mc_korall_api',
    'pass': 'korall123api'
}

# ID в moneyCare
MONEY_CARE_POINT_ID = '260620181431'

# урл на основной сайт используется в заявке Money Care
MAIN_DOMAIN_FRONTED_URL = 'http://www.korallmicro.ru'

MANAGER_MONEY_CARE = ['kaduk_ia@km-union.ru']