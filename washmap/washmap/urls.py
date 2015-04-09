from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import (
    WashMapStaticView,
    WashMapServerView,
    LineStaticView,
)

urlpatterns = patterns('',
    url(r'^$', WashMapServerView.as_view(), name='server'),
    url(r'^static$', WashMapStaticView.as_view(), name='home'),
    url(r'^line$', LineStaticView.as_view(), name='line'),
)
