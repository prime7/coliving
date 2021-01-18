from decouple import config

if config('DEBUG'):
    EASYPOST_KEY = config('EASYPOST_SECRET_KEY_DEBUG')
else:
    EASYPOST_KEY = config('EASYPOST_SECRET_KEY_PROD')
    