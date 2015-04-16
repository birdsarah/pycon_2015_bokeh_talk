import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

from dj_static import Cling
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = Cling(get_wsgi_application())
application = DjangoWhiteNoise(application)

