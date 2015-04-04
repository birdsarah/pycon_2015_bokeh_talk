from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import (
    WashMapStaticView,
    WashMapServerView,
)

urlpatterns = patterns('',
    url(r'^$', WashMapStaticView.as_view(), name='home'),
    url(r'^server$', WashMapServerView.as_view(), name='server'),
)
