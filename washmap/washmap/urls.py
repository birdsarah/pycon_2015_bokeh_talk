from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import (
    LineView,
)

urlpatterns = patterns('',
    url(r'^$', LineView.as_view(), name='home'),
)
