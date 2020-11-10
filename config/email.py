from decouple import config
import os


if 'RDS_DB_NAME' in os.environ: 
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_PORT = config('EMAIL_PORT')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
else:    
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
