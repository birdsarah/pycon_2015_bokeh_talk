from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import (
    ChartView,
    GettingStarted,
)

urlpatterns = patterns('',
    url(r'^$', ChartView.as_view(), name='home'),
    url(r'^getting-started$', GettingStarted.as_view(), name='home'),
)
