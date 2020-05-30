from decouple import config
import os
from .settings import BASE_DIR


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = None
AWS_STATIC_LOCATION = 'static'


if config('DEBUG')=='True': 
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    MEDIA_URL = '/media/'   
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
    DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'
    STATICFILES_STORAGE = 'config.storage_backends.StaticStorage'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_root'), ]