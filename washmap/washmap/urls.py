from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import (
    WashMapStaticView,
)

urlpatterns = patterns('',
    url(r'^$', WashMapStaticView.as_view(), name='home'),
)
