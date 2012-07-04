try:
    from settings_default import *
except ImportError:
    pass

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/tmp/registro',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
"""
"""
STATIC_URL_PATH = 'static'
STATIC_URL = 'http://localhost:8080/' + STATIC_URL_PATH + '/'
STATIC_DOC_ROOT = os.path.join(PROJECT_ROOT, 'static')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'xxx@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxxx'
EMAIL_PORT = 587
EMAIL_FROM = 'xxx@gmail.com'

BASE_URL = 'http://localhost:8080/'

"""
