import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
WASHMAP_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir, 'washmap'))
sys.path.append(WASHMAP_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

from dj_static import Cling
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = Cling(get_wsgi_application())
application = DjangoWhiteNoise(application)

