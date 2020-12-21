INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'accounts',
    'rentals',
    'memberships',
    'agreements',
    'services',
    'faq',
    'finances',
    'dashboards',
    'rentanything',
    'buyandsell',
    'deliveranything',

    'crispy_forms',
    'storages',
    'meta',
    'robots',
    'rest_framework',
    'easypost',
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ]
}