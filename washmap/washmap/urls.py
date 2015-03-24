from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import (
    ChartView,
    GettingStarted,
    WashMapServerView,
    WashMapStaticView,
)

urlpatterns = patterns('',
    url(r'^$', ChartView.as_view(), name='home'),
    url(r'^washmap-static$', WashMapStaticView.as_view(), name='washmap-static'),
    url(r'^washmap-server$', WashMapServerView.as_view(), name='washmap-server'),
    url(r'^lines$', GettingStarted.as_view(), name='lines'),
)
