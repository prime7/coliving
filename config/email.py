from decouple import config


# if config('DEBUG'): 
#     EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# else:

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')