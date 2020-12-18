# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ukrchitrade',
        'USER' : 'rostislav',
        'PASSWORD' : 'streetride24',
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}
