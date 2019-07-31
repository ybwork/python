DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'marketplace',
        'USER': 'postgres',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}