EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'i.am.kalchenko@gmail.com'
EMAIL_HOST_PASSWORD = '99011qwevbn'
EMAIL_PORT = 587

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'komitet',
        'USER': 'ik',
        'PASSWORD': '1234pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
