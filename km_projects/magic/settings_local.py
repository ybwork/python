# -*- coding: utf-8 -*-
import os

CONF_PATH = os.path.dirname(__file__)
BASE_URL = 'http://magic.km-union.ru'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGIN_URL = '/login/'

# Адреса для доступа к debug-tool-bar если debug=True
INTERNAL_IPS = (
    '*',
)


ALLOW_IPS_FOR_API = ['127.0.0.1', '192.168.7.3', '*']

ADMINS = (
    ('Kaduk_IA', 'kaduk_ia@km-union.ru'),
)

MANAGERS = (
    ('Kaduk_IA', 'kaduk_ia@km-union.ru'),
)

ALLOWED_HOSTS = [
    '*',
]

LOCAL_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'magic',
        'USER': 'root',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        # InnoDB для решения проблем с ForeignKey, constraint и т.п.
        'OPTIONS': {
            # 'read_default_file': os.path.join(CONF_PATH, 'my.cnf'),
            'init_command': 'SET default_storage_engine=INNODB',
        }
    },
    # TODO: Возможно не используется
    # 'online_shop_info': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'online_shop_info',
    #     'USER': 'root',
    #     'PASSWORD': 'asdf1234',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         # 'read_default_file': os.path.join(CONF_PATH, 'online_shop_info.cnf'),
    #         'init_command': 'SET default_storage_engine=INNODB',
    #     }
    # },
    # TODO: Возможно не используется и в будущем должна исчезнуть
    'istore': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'istore',
        'USER': 'root',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            # 'read_default_file': os.path.join(CONF_PATH, 'istore.cnf'),
            'init_command': 'SET default_storage_engine=INNODB',
        }
    },
    # TODO: Возможно не используется
    # 'goods_office': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'goods_office',
    #     'USER': 'root',
    #     'PASSWORD': 'asdf1234',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         # 'read_default_file': os.path.join(CONF_PATH, 'goods_office.cnf'),
    #         'init_command': 'SET default_storage_engine=INNODB',
    #     }
    # },
    # TODO: Возможно не используется
    # '1c': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': '1c',
    #     'USER': 'root',
    #     'PASSWORD': 'asdf1234',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         # 'read_default_file': os.path.join(CONF_PATH, '1c.cnf'),
    #         'init_command': 'SET default_storage_engine=INNODB',
    #     }
    # },
    '1c_8_raw': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '1c_8_raw',
        'USER': 'root',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            # 'read_default_file': os.path.join(CONF_PATH, '1c_8_raw.cnf'),
            'init_command': 'SET default_storage_engine=INNODB',
        }
    },
    'korallmicro': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'korallmicro',
        'USER': 'postgres',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
    'snr_new': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'snr',
        'USER': 'postgres',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'sales_base_models': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'snr',
        'USER': 'postgres',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}


ROUTERS = {}
ROUTERS['raw_processing'] = {
    'db_for_read': '1c_8_raw',
    'allow_syncdb': False
}
# TODO: Возможно не используется и в будущем должна исчезнуть
ROUTERS['istore'] = {
    'db_for_read': 'istore',
    'db_for_write': 'istore',
    'allow_syncdb': False
}

SECRET_KEY = '@v{Z6qxAsD/j*jD<qq4@o,?L[5@ALP#REVo881"Q3Y7~*2k|'

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
        'cards.tasks': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp1.km-union.ru'
SERVER_EMAIL = 'magic_local@error'


CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 2
CELERY_SEND_TASK_ERROR_EMAILS = True

# параметр нужен для работы мониторинга типа celery flower
CELERY_SEND_EVENTS = False


BROKER_URL = [
    # Важно, чтобы на dev был localhost
    "amqp://rabbitmq:rabbitmq@localhost:5672/magic"
]

BROKER_TARGET_URL = [
    # Важно, чтобы на dev был localhost
    "amqp://rabbitmq:rabbitmq@localhost:5672/broker"
]


CELERY_ACCEPT_CONTENT = ['json', 'pickle']

# задежрка в часах для выгрузки из 1С товара для magic
DELAY_HOURS_FOR_UNLOADING_FROM_1C = 12

# Величина разброса (в процентах) количества распределенных товаров
DISPERSION_LEFT_VALUE_OF_DISTRIBUTED_PRODUCT_IN_PERCENT = 2
DISPERSION_RIGHT_VALUE_OF_DISTRIBUTED_PRODUCT_IN_PERCENT = 5

# Номера телефонов для оповещения в случае ошибки в распределении
SYNCHRONIZATION_NOTIFICATION_PHONE_NUMBERS = []

# Группа для рассылки системных сообщений
SYSTEM_NOTIFICATION_EMAIL_GROUPS = ['kaduk_ia@km-union.ru']

# Группа для рассылки контент менеджерам для каждого типа магазина
CONTENT_MANAGER_NOTIFICATION_EMAIL_GROUPS = {
    'korallmicro': ['kaduk_ia@km-union.ru'],
    'istore': [],
    'snr_new': [],
}

# Группа для рассылки ответственных за обзоры
REVIEW_CHECKER_NOTIFICATION_EMAIL_GROUPS = []

# Группа для рассылки ответственных за выгодные предложения
OFFERS_CHECKER_NOTIFICATION_EMAIL_GROUPS = []

# Группа для рассылки ответственных за каталогом
UNIQUE_FULL_ALIAS_CHECKER_NOTIFICATION_EMAIL_GROUPS = []

# Группа для рассылки ответственные за смену актуальности
ACTUAL_CHECKER_NOTIFICATION_EMAIL_GROUPS = []

# Абсолютный путь к папке images сайта korallmicro
PATH_TO_KORALLMICRO = '/media/storage/korallmicro/images/'

# Абсолютный путь к папке images сайта istore
PATH_TO_ISTORE = '/media/storage/istore/images/'

# Абсолютный путь к папке images сайта snr
PATH_TO_SNR = '/media/storage/snr/images/'

# Абсолютный путь к папки media хранилица на cdn
PATH_TO_STORAGE = '/media/storage/magic/'

STORE_UID = '1bab7b05-b1fc-11e2-93f1-002655df3ac1'

# Группа для рассылки статистики по конфигуратору
CONFIGURATOR_ANALITICS = []

SITE_PRODUCTS_REPORT_EMAILS = ['kaduk_ia@km-union.ru']

CRITICAL_ERROR_EMAIL_GROUPS = {
    'phones': [],
    'emails': [
        'kaduk_ia@km-union.ru',
    ]
}

EXTERN_SITE_CONFIG = {
    'korallmicro': {
        'main_site_id': 49,
    },
    'snr_new': {
        'main_site_id': 16,
        'sites': {
            1: {
                'stores': {
                    'f5c8676c-2563-11e5-80d9-001b21d8d330': u'SNR-Коммунаров (ячеистый склад)',
                    'bee7a5c8-249c-11e5-80d9-001b21d8d330': u'SNR-Коммунаров 268 Витрина',
                    'dddf5e4d-249c-11e5-80d9-001b21d8d330': u'SNR-Красных Партизан',
                    'd024f27e-249c-11e5-80d9-001b21d8d330': u'SNR-Лузана',
                    '6e5b36dc-4c85-11e5-93f1-001b21d8d330': u'SNR-Производство ВТ',
                    'ec34c5eb-249c-11e5-80d9-001b21d8d330': u'SNR-Тургенева',
                },
                'prices': {
                    'd0941d18-92d6-4ffa-9498-b977014ce84e': u'Интернет СНР',
                    '5e2b2da4-cbf7-4793-b6ad-a40bf98aa497': u'Розничная Краснодар'
                }
            },
            2: {
                'stores': {
                    'f996fb5c-249c-11e5-80d9-001b21d8d330': u'SNR-Анапа',
                },
                'prices': {
                    'd0941d18-92d6-4ffa-9498-b977014ce84e': u'Интернет СНР',
                    'c28e46e0-c74e-4f67-a868-631edda27a61': u'Розничная Анапа'
                }
            },
        },
    }
}

# Склад КМ
STORE_UUID = '1bab7b05-b1fc-11e2-93f1-002655df3ac1'

# глобальная и групповая наценка для синхронизации с istore
ADDITIONAL_COST_FOR_ISTORE = {
    'global': 7.0,
    'group': {
        '0064d6f8-743c-11e6-9400-001b21d8d330': 0.0,
    },
    'rrs': [
        160344, 191242, 191240, 175920, 191241, 192055,
        180247,
        181076,
    ]
}


COUNT_ITERATED = 10
