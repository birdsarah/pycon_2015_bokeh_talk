from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import (
    ChartView,
    GettingStarted,
    WashMapView,
)

urlpatterns = patterns('',
    url(r'^$', ChartView.as_view(), name='home'),
    url(r'^washmap$', WashMapView.as_view(), name='washmap'),
    url(r'^lines$', GettingStarted.as_view(), name='lines'),
)
