from .base import *

DEBUG = False

ALLOWED_HOSTS = ['django-jchart.matthisk.nl']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
AWS_STORAGE_BUCKET_NAME = 'django-jchart'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_PRELOAD_METADATA = True
AWS_S3_HOST = 's3-eu-central-1.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = '%s.%s' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_HOST)

STATIC_URL = "//%s/" % AWS_S3_CUSTOM_DOMAIN

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
