from ..settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
	'localhost',
	'.pythonanywhere.com',
]

SECRET_KEY = get_env_variable("SECRET_KEY")

STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"